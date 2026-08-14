"""Deterministic client onboarding helpers."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.bootstrap_client import bootstrap_client, validate_client_id

SENSITIVITY = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "CUI"}
SOURCE_EXTENSIONS = {
    ".md": "meeting-notes",
    ".txt": "notes",
    ".doc": "document",
    ".docx": "document",
    ".pdf": "document",
    ".ppt": "presentation",
    ".pptx": "presentation",
    ".xls": "spreadsheet",
    ".xlsx": "spreadsheet",
    ".csv": "spreadsheet",
    ".tsv": "spreadsheet",
    ".png": "screenshot-or-diagram",
    ".jpg": "screenshot-or-diagram",
    ".jpeg": "screenshot-or-diagram",
    ".svg": "diagram",
    ".vsdx": "diagram",
    ".json": "configuration-export",
    ".yaml": "configuration-export",
    ".yml": "configuration-export",
    ".xml": "configuration-export",
}


@dataclass(frozen=True)
class OnboardingResult:
    client_slug: str
    workspace: Path
    created_workspace: bool
    sources_cataloged: int
    sources_skipped: int
    open_questions: list[str]


def slugify_client_name(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    if len(slug) > 64:
        slug = slug[:64].strip("-")
    validate_client_id(slug)
    return slug


def onboard_client(
    root: Path,
    client_name: str,
    engagement_name: str | None = None,
    engagement_type: str | None = None,
    frameworks: list[str] | None = None,
    source_paths: list[Path] | None = None,
    consultant: str | None = None,
    sensitivity: str = "CONFIDENTIAL",
    slug: str | None = None,
    runtime: str = "unknown",
) -> OnboardingResult:
    root = root.resolve()
    frameworks = frameworks or []
    source_paths = source_paths or []
    if sensitivity not in SENSITIVITY:
        raise ValueError(f"Unsupported sensitivity: {sensitivity}")

    client_slug = slug or slugify_client_name(client_name)
    validate_client_id(client_slug)
    workspace = root / "clients" / client_slug
    created_workspace = False

    if not workspace.exists():
        bootstrap_client(client_slug, root)
        created_workspace = True

    _ensure_onboarding_dirs(workspace)
    _write_client_yaml(
        workspace=workspace,
        client_name=client_name,
        client_slug=client_slug,
        sensitivity=sensitivity,
    )
    _write_engagement_yaml(
        workspace=workspace,
        engagement_name=engagement_name,
        engagement_type=engagement_type,
        frameworks=frameworks,
        consultant=consultant,
        sensitivity=sensitivity,
    )

    cataloged, skipped = catalog_sources(
        root=root,
        workspace=workspace,
        client_slug=client_slug,
        engagement_name=engagement_name,
        source_paths=source_paths,
        classification=sensitivity,
        runtime=runtime,
    )
    open_questions = write_open_questions(workspace)
    write_onboarding_status(
        workspace=workspace,
        created_workspace=created_workspace,
        sources_cataloged=cataloged,
        sources_skipped=skipped,
        open_questions=open_questions,
    )
    log_activity(
        workspace,
        {
            "actor": "agent",
            "runtime": runtime,
            "action": "onboarding_run",
            "client": client_slug,
            "sources_cataloged": cataloged,
            "sources_skipped": skipped,
        },
    )
    return OnboardingResult(
        client_slug=client_slug,
        workspace=workspace,
        created_workspace=created_workspace,
        sources_cataloged=cataloged,
        sources_skipped=skipped,
        open_questions=open_questions,
    )


def catalog_sources(
    root: Path,
    workspace: Path,
    client_slug: str,
    engagement_name: str | None,
    source_paths: list[Path],
    classification: str,
    runtime: str,
) -> tuple[int, int]:
    catalog_path = workspace / "sources" / "catalog.jsonl"
    existing = _read_catalog(catalog_path)
    existing_keys = {
        (entry.get("original_path"), entry.get("hash")) for entry in existing
    }
    next_number = _next_source_number(existing)
    cataloged = 0
    skipped = 0
    now = datetime.now(UTC).isoformat()

    for source_path in _iter_source_files(source_paths):
        source_hash = _sha256(source_path)
        original_path = _display_path(root, source_path)
        key = (original_path, source_hash)
        if key in existing_keys:
            skipped += 1
            continue

        source_id = f"SRC-{next_number:04d}"
        next_number += 1
        entry = {
            "source_id": source_id,
            "filename": source_path.name,
            "source_type": classify_source(source_path),
            "original_path": original_path,
            "client": client_slug,
            "engagement": engagement_name,
            "classification": classification,
            "ingested_at": now,
            "hash": source_hash,
            "size_bytes": source_path.stat().st_size,
        }
        _append_jsonl(catalog_path, entry)
        log_activity(
            workspace,
            {
                "actor": "agent",
                "runtime": runtime,
                "action": "source_cataloged",
                "source_id": source_id,
                "path": original_path,
            },
        )
        cataloged += 1

    return cataloged, skipped


def validate_client_workspace(
    root: Path, client_slug: str
) -> tuple[list[str], list[str]]:
    workspace = root.resolve() / "clients" / client_slug
    errors: list[str] = []
    warnings: list[str] = []
    if not workspace.exists():
        return [f"client workspace does not exist: clients/{client_slug}"], warnings

    required_dirs = [
        "context",
        "sources",
        "evidence",
        "working",
        "deliverables",
        "decisions",
        "retrieval",
        "logs",
        "onboarding",
    ]
    for directory in required_dirs:
        if not (workspace / directory).is_dir():
            errors.append(f"missing directory: clients/{client_slug}/{directory}")

    schemas = {
        "client.yaml": root / "schemas" / "client.schema.json",
        "engagement.yaml": root / "schemas" / "engagement.schema.json",
    }
    for filename, schema_path in schemas.items():
        target = workspace / filename
        if not target.exists():
            errors.append(f"missing file: clients/{client_slug}/{filename}")
            continue
        errors.extend(_validate_yaml_schema(target, schema_path))

    catalog_path = workspace / "sources" / "catalog.jsonl"
    if catalog_path.exists():
        source_schema = _read_json(root / "schemas" / "source.schema.json")
        validator = Draft202012Validator(source_schema)
        seen_source_ids: set[str] = set()
        for line_number, entry in _iter_jsonl(catalog_path):
            for error in validator.iter_errors(entry):
                errors.append(
                    f"{catalog_path.relative_to(root)}:{line_number}: {error.message}"
                )
            source_id = str(entry.get("source_id"))
            if source_id in seen_source_ids:
                errors.append(f"duplicate source_id in catalog: {source_id}")
            seen_source_ids.add(source_id)
            original_value = entry.get("original_path")
            original = (
                Path(str(original_value)).expanduser() if original_value else None
            )
            if original and not original.is_absolute():
                original = root / original
            if original and original.is_file():
                actual_hash = _sha256(original)
                if actual_hash != entry.get("hash"):
                    errors.append(f"source hash mismatch: {source_id}")
            elif original:
                warnings.append(
                    f"source original path not available on this machine: {source_id}"
                )
    else:
        errors.append(f"missing file: clients/{client_slug}/sources/catalog.jsonl")

    return errors, warnings


def write_open_questions(workspace: Path) -> list[str]:
    engagement = _read_yaml(workspace / "engagement.yaml")
    questions = []
    required_questions = {
        "stakeholders": "Who are the primary client stakeholders and decision makers?",
        "objectives": "What specific outcomes should this engagement produce?",
        "scope": "Which business units, systems, and environments are in scope?",
        "out_of_scope": "What is explicitly out of scope?",
        "deliverables": (
            "Which deliverables are expected and what are their acceptance criteria?"
        ),
        "important_dates": (
            "What kickoff, interview, evidence, draft, and final delivery dates matter?"
        ),
        "known_systems": (
            "Which systems, applications, and infrastructure components are known?"
        ),
        "business_units": "Which business units or locations are relevant?",
        "data_handling": (
            "What confidentiality, CUI, PII, or local-only handling rules apply?"
        ),
    }
    for key, question in required_questions.items():
        if not engagement.get(key):
            questions.append(question)

    target = workspace / "onboarding" / "open-questions.md"
    body = "\n".join(f"- [ ] {question}" for question in questions) or "- None."
    target.write_text(
        f"""# Open Onboarding Questions

These questions should be answered by the consultant or validated from source material.
Do not let an AI model silently convert unanswered questions into facts.

{body}
""",
        encoding="utf-8",
    )
    return questions


def write_onboarding_status(
    workspace: Path,
    created_workspace: bool,
    sources_cataloged: int,
    sources_skipped: int,
    open_questions: list[str],
) -> None:
    status = {
        "onboarding": {
            "status": "incomplete" if open_questions else "ready-for-analysis",
            "updated_at": datetime.now(UTC).isoformat(),
            "workspace_initialized": True,
            "created_workspace_this_run": created_workspace,
            "sources_cataloged_this_run": sources_cataloged,
            "sources_skipped_this_run": sources_skipped,
            "open_question_count": len(open_questions),
        }
    }
    _write_yaml(workspace / "onboarding" / "status.yaml", status)


def log_activity(workspace: Path, event: dict[str, Any]) -> None:
    entry = {"timestamp": datetime.now(UTC).isoformat(), **event}
    _append_jsonl(workspace / "logs" / "activity.jsonl", entry)


def classify_source(path: Path) -> str:
    name = path.name.lower()
    if "policy" in name:
        return "policy"
    if "procedure" in name:
        return "procedure"
    if "diagram" in name or "architecture" in name:
        return "diagram"
    if "evidence" in name:
        return "evidence"
    if "kickoff" in name or "meeting" in name or "interview" in name:
        return "meeting-notes"
    if "sow" in name or "statement-of-work" in name:
        return "sow"
    return SOURCE_EXTENSIONS.get(path.suffix.lower(), "unknown")


def create_client_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create or continue a consulting client onboarding workspace."
    )
    parser.add_argument(
        "client_name", help="Client display name, e.g. Acme Corporation"
    )
    parser.add_argument("--slug", help="Override generated client slug")
    parser.add_argument("--engagement-name")
    parser.add_argument("--engagement-type")
    parser.add_argument("--framework", action="append", default=[])
    parser.add_argument("--source", action="append", type=Path, default=[])
    parser.add_argument("--consultant")
    parser.add_argument(
        "--classification",
        default="CONFIDENTIAL",
        choices=sorted(SENSITIVITY),
        help="Default sensitivity for created metadata and source catalog entries.",
    )
    parser.add_argument("--runtime", default="manual-cli")
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    return parser


def validate_workspace_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a client onboarding workspace."
    )
    parser.add_argument("client_slug")
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    return parser


def run_create_client(argv: list[str] | None = None) -> int:
    parser = create_client_parser()
    args = parser.parse_args(argv)
    try:
        result = onboard_client(
            root=args.root,
            client_name=args.client_name,
            engagement_name=args.engagement_name,
            engagement_type=args.engagement_type,
            frameworks=args.framework,
            source_paths=args.source,
            consultant=args.consultant,
            sensitivity=args.classification,
            slug=args.slug,
            runtime=args.runtime,
        )
    except (ValueError, FileNotFoundError) as exc:
        parser.exit(2, f"error: {exc}\n")

    print(f"Client: {result.client_slug}")
    print(f"Workspace: {result.workspace}")
    print(f"Workspace initialized: {result.created_workspace}")
    print(f"Sources cataloged: {result.sources_cataloged}")
    print(f"Sources skipped: {result.sources_skipped}")
    print(f"Open onboarding questions: {len(result.open_questions)}")
    print("Next steps:")
    print(f"  1. Review clients/{result.client_slug}/onboarding/open-questions.md")
    print(f"  2. Review clients/{result.client_slug}/sources/catalog.jsonl")
    print(f"  3. Run: scripts/validate-workspace {result.client_slug}")
    return 0


def run_validate_workspace(argv: list[str] | None = None) -> int:
    parser = validate_workspace_parser()
    args = parser.parse_args(argv)
    errors, warnings = validate_client_workspace(args.root, args.client_slug)
    for warning in warnings:
        print(f"warning: {warning}")
    if errors:
        print("Workspace validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Workspace validation passed.")
    return 0


def _ensure_onboarding_dirs(workspace: Path) -> None:
    for directory in [
        "intake",
        "sources",
        "working",
        "deliverables",
        "decisions",
        "retrieval",
        "logs",
        "onboarding",
        "frameworks",
    ]:
        (workspace / directory).mkdir(parents=True, exist_ok=True)
    for jsonl in [
        workspace / "sources" / "catalog.jsonl",
        workspace / "logs" / "activity.jsonl",
    ]:
        jsonl.touch(exist_ok=True)


def _write_client_yaml(
    workspace: Path,
    client_name: str,
    client_slug: str,
    sensitivity: str,
) -> None:
    path = workspace / "client.yaml"
    existing = _read_yaml(path) if path.exists() else {}
    existing_client = existing.get("client", {})
    existing_name = existing_client.get("name")
    preserved_name = (
        existing_name
        if existing_name
        and existing_name not in {client_slug, "{{CLIENT_ID}}", "TBD"}
        else client_name
    )
    data = {
        "client": {
            "name": preserved_name,
            "slug": client_slug,
            "status": existing_client.get("status", "active"),
        },
        "classification": existing.get("classification", sensitivity),
        "created": existing.get(
            "created", {"date": datetime.now(UTC).date().isoformat()}
        ),
    }
    _write_yaml(path, _deep_merge(existing, data))


def _write_engagement_yaml(
    workspace: Path,
    engagement_name: str | None,
    engagement_type: str | None,
    frameworks: list[str],
    consultant: str | None,
    sensitivity: str,
) -> None:
    path = workspace / "engagement.yaml"
    existing = _read_yaml(path) if path.exists() else {}
    current_frameworks = list(existing.get("frameworks", []))
    for framework in frameworks:
        normalized = framework.strip().lower()
        if normalized and normalized not in current_frameworks:
            current_frameworks.append(normalized)

    engagement = existing.get("engagement", {})
    data = {
        "engagement": {
            "name": _prefer_existing(engagement.get("name"), engagement_name),
            "type": _prefer_existing(engagement.get("type"), engagement_type),
            "status": engagement.get("status", "onboarding"),
        },
        "consultant": existing.get("consultant") or consultant,
        "frameworks": current_frameworks,
        "classification": existing.get("classification", sensitivity),
        "created": existing.get(
            "created", {"date": datetime.now(UTC).date().isoformat()}
        ),
        "stakeholders": existing.get("stakeholders", []),
        "objectives": existing.get("objectives", []),
        "scope": existing.get("scope", []),
        "out_of_scope": existing.get("out_of_scope", []),
        "deliverables": existing.get("deliverables", []),
        "important_dates": existing.get("important_dates", []),
        "known_systems": existing.get("known_systems", []),
        "business_units": existing.get("business_units", []),
        "data_handling": existing.get("data_handling"),
    }
    _write_yaml(path, data)


def _iter_source_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        expanded = path.expanduser().resolve()
        if not expanded.exists():
            raise FileNotFoundError(f"source path does not exist: {path}")
        if expanded.is_file():
            files.append(expanded)
        else:
            for candidate in sorted(expanded.rglob("*")):
                if candidate.is_file() and not candidate.name.startswith("."):
                    files.append(candidate)
    return sorted(files)


def _read_catalog(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [entry for _, entry in _iter_jsonl(path)]


def _iter_jsonl(path: Path) -> list[tuple[int, dict[str, Any]]]:
    entries: list[tuple[int, dict[str, Any]]] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line.strip():
            continue
        entries.append((line_number, json.loads(line)))
    return entries


def _next_source_number(entries: list[dict[str, Any]]) -> int:
    highest = 0
    for entry in entries:
        match = re.fullmatch(r"SRC-(\d{4})", str(entry.get("source_id", "")))
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def _append_jsonl(path: Path, entry: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _display_path(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")
    return loaded


def _write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_yaml_schema(yaml_path: Path, schema_path: Path) -> list[str]:
    errors: list[str] = []
    instance = _read_yaml(yaml_path)
    schema = _read_json(schema_path)
    validator = Draft202012Validator(schema)
    for error in validator.iter_errors(instance):
        errors.append(f"{yaml_path.name}: {error.message}")
    return errors


def _deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _prefer_existing(existing: Any, supplied: str | None) -> str:
    if existing and str(existing).strip().upper() != "TBD":
        return str(existing)
    return supplied or "TBD"

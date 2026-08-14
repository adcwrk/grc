#!/usr/bin/env python3
"""Validate repository structure, metadata, and internal references."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from retrieval.loaders.markdown import parse_markdown_file

REQUIRED_DIRS = [
    "docs",
    "knowledge",
    "clients/_template/context",
    "templates",
    "agents",
    "prompts",
    "schemas",
    "retrieval",
    "scripts",
]
SENSITIVITY = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "CUI"}
REQUIRED_BY_TYPE = {
    "evidence": {"artifact_id", "artifact_type", "client", "status", "sensitivity"},
    "finding": {"artifact_id", "artifact_type", "client", "status", "sensitivity"},
    "decision": {"artifact_id", "artifact_type", "client", "status", "sensitivity"},
    "task": {"artifact_id", "artifact_type", "client", "status", "sensitivity"},
    "context": {"artifact_id", "artifact_type", "client", "status", "sensitivity"},
    "handoff": {"artifact_id", "artifact_type", "client", "status", "sensitivity"},
}
LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for directory in REQUIRED_DIRS:
        if not (root / directory).is_dir():
            errors.append(f"missing required directory: {directory}")

    clients = {
        path.name
        for path in (root / "clients").glob("*")
        if path.is_dir() and not path.name.startswith("_")
    }

    artifact_ids: dict[str, list[Path]] = defaultdict(list)
    evidence_ids: set[str] = set()
    referenced_evidence: set[str] = set()

    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if ".git" in relative.parts:
            continue

        try:
            artifact = parse_markdown_file(path)
        except ValueError as exc:
            errors.append(f"{relative}: invalid front matter: {exc}")
            continue

        metadata = artifact.metadata
        artifact_id = metadata.get("artifact_id")
        artifact_type = metadata.get("artifact_type")
        if artifact_id:
            artifact_ids[str(artifact_id)].append(relative)
        if artifact_type in REQUIRED_BY_TYPE:
            missing = REQUIRED_BY_TYPE[str(artifact_type)] - set(metadata)
            for key in sorted(missing):
                errors.append(f"{relative}: missing metadata field: {key}")

        client = metadata.get("client")
        is_template_example = (
            "templates" in relative.parts and client == "example-client"
        )
        if client and client not in {
            "{{CLIENT_ID}}",
            "repository",
        } and client not in clients and not is_template_example:
            errors.append(f"{relative}: unknown client reference: {client}")

        sensitivity = metadata.get("sensitivity")
        if sensitivity and sensitivity not in SENSITIVITY:
            errors.append(f"{relative}: invalid sensitivity: {sensitivity}")

        if artifact_type == "evidence" and artifact_id:
            evidence_ids.add(str(artifact_id))

        for evid in _as_list(metadata.get("evidence")):
            referenced_evidence.add(str(evid))

        if artifact_type == "finding":
            if not metadata.get("requirement") and not metadata.get("control"):
                errors.append(
                    f"{relative}: finding missing requirement/control reference"
                )

        if artifact_type == "evidence":
            has_location = metadata.get("evidence_location") or metadata.get(
                "source_system"
            )
            if not has_location:
                errors.append(
                    f"{relative}: evidence missing source_system or evidence_location"
                )

        for link in LINK_RE.findall(artifact.body):
            link_path = link.split("#", 1)[0]
            if not link_path:
                continue
            target = (path.parent / link_path).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{relative}: link escapes repository: {link}")
                continue
            if not target.exists():
                errors.append(f"{relative}: broken internal link: {link}")

    for artifact_id, paths in sorted(artifact_ids.items()):
        if len(paths) > 1:
            joined = ", ".join(path.as_posix() for path in paths)
            errors.append(f"duplicate artifact_id {artifact_id}: {joined}")

    for evidence_id in sorted(referenced_evidence - evidence_ids):
        errors.append(f"dangling evidence reference: {evidence_id}")

    return errors


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate GRC repository structure.")
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

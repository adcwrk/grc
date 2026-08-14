from pathlib import Path

import yaml

from scripts.onboarding import (
    onboard_client,
    slugify_client_name,
    validate_client_workspace,
)


def make_template(root: Path) -> None:
    template = root / "clients" / "_template"
    (template / "context").mkdir(parents=True)
    for directory in [
        "sources",
        "logs",
        "onboarding",
        "evidence",
        "working",
        "deliverables",
        "decisions",
        "retrieval",
    ]:
        (template / directory).mkdir(parents=True)
    (template / "context" / "project-context.md").write_text(
        "---\nartifact_id: CTX-{{CLIENT_ID}}\nartifact_type: context\n"
        "client: {{CLIENT_ID}}\nstatus: draft\nsensitivity: INTERNAL\n---\n",
        encoding="utf-8",
    )
    (template / "client.yaml").write_text(
        "client:\n  name: \"{{CLIENT_ID}}\"\n  slug: \"{{CLIENT_ID}}\"\n"
        "  status: active\nclassification: INTERNAL\ncreated:\n"
        "  date: \"{{CREATED_DATE}}\"\n",
        encoding="utf-8",
    )
    (template / "engagement.yaml").write_text(
        "engagement:\n  name: TBD\n  type: TBD\n  status: onboarding\n"
        "frameworks: []\nclassification: INTERNAL\ncreated:\n"
        "  date: \"{{CREATED_DATE}}\"\n",
        encoding="utf-8",
    )


def copy_schemas(root: Path, repo_root: Path) -> None:
    schema_dir = root / "schemas"
    schema_dir.mkdir()
    for name in [
        "client.schema.json",
        "engagement.schema.json",
        "source.schema.json",
    ]:
        (schema_dir / name).write_text(
            (repo_root / "schemas" / name).read_text(encoding="utf-8"),
            encoding="utf-8",
        )


def test_slugify_client_name() -> None:
    assert slugify_client_name("Acme Corporation, Inc.") == "acme-corporation-inc"


def test_onboard_client_catalogs_sources(tmp_path: Path) -> None:
    make_template(tmp_path)
    copy_schemas(tmp_path, Path.cwd())
    intake = tmp_path / "intake" / "acme"
    intake.mkdir(parents=True)
    (intake / "kickoff-notes.md").write_text("Kickoff notes", encoding="utf-8")
    (intake / "security-policy.pdf").write_bytes(b"policy")

    result = onboard_client(
        root=tmp_path,
        client_name="Acme Corporation",
        engagement_name="CMMC Readiness",
        engagement_type="assessment",
        frameworks=["cmmc", "nist-csf-2.0"],
        source_paths=[intake],
        consultant="Consultant",
        runtime="pytest",
    )

    assert result.client_slug == "acme-corporation"
    assert result.sources_cataloged == 2
    client_yaml = yaml.safe_load(
        (result.workspace / "client.yaml").read_text(encoding="utf-8")
    )
    engagement_yaml = yaml.safe_load(
        (result.workspace / "engagement.yaml").read_text(encoding="utf-8")
    )
    assert client_yaml["client"]["name"] == "Acme Corporation"
    assert engagement_yaml["engagement"]["name"] == "CMMC Readiness"
    assert engagement_yaml["frameworks"] == ["cmmc", "nist-csf-2.0"]

    catalog = (result.workspace / "sources" / "catalog.jsonl").read_text(
        encoding="utf-8"
    )
    assert "SRC-0001" in catalog
    assert "SRC-0002" in catalog


def test_onboarding_is_idempotent_for_existing_sources(tmp_path: Path) -> None:
    make_template(tmp_path)
    copy_schemas(tmp_path, Path.cwd())
    intake = tmp_path / "intake"
    intake.mkdir()
    (intake / "diagram.png").write_bytes(b"diagram")

    first = onboard_client(
        root=tmp_path,
        client_name="Acme Corporation",
        source_paths=[intake],
        runtime="pytest",
    )
    second = onboard_client(
        root=tmp_path,
        client_name="Acme Corporation",
        source_paths=[intake],
        runtime="pytest",
    )

    assert first.sources_cataloged == 1
    assert second.sources_cataloged == 0
    assert second.sources_skipped == 1


def test_validate_client_workspace(tmp_path: Path) -> None:
    make_template(tmp_path)
    copy_schemas(tmp_path, Path.cwd())
    onboard_client(root=tmp_path, client_name="Acme Corporation", runtime="pytest")

    errors, warnings = validate_client_workspace(tmp_path, "acme-corporation")

    assert errors == []
    assert warnings == []


def test_validate_workspace_rejects_bad_source_catalog(tmp_path: Path) -> None:
    make_template(tmp_path)
    copy_schemas(tmp_path, Path.cwd())
    result = onboard_client(root=tmp_path, client_name="Acme Corporation")
    (result.workspace / "sources" / "catalog.jsonl").write_text(
        '{"source_id": "bad"}\n',
        encoding="utf-8",
    )

    errors, _ = validate_client_workspace(tmp_path, "acme-corporation")

    assert any("does not match" in error or "required" in error for error in errors)

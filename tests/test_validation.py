from pathlib import Path

from scripts.validate_repository import validate


def create_required_dirs(root: Path) -> None:
    for directory in [
        "docs",
        "knowledge",
        "clients/_template/context",
        "templates",
        "agents",
        "prompts",
        "schemas",
        "retrieval",
        "scripts",
    ]:
        (root / directory).mkdir(parents=True, exist_ok=True)


def test_duplicate_ids(tmp_path: Path) -> None:
    create_required_dirs(tmp_path)
    for name in ["a.md", "b.md"]:
        (tmp_path / name).write_text(
            "---\nartifact_id: DUP-1\nartifact_type: note\nstatus: draft\n"
            "sensitivity: INTERNAL\n---\n",
            encoding="utf-8",
        )

    errors = validate(tmp_path)

    assert any("duplicate artifact_id DUP-1" in error for error in errors)


def test_invalid_references(tmp_path: Path) -> None:
    create_required_dirs(tmp_path)
    path = tmp_path / "clients" / "_template" / "context" / "note.md"
    path.write_text(
        "---\nartifact_id: NOTE-1\nartifact_type: note\nstatus: draft\n"
        "sensitivity: INTERNAL\n---\n[missing](missing.md)\n",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert any("broken internal link" in error for error in errors)


def test_dangling_evidence_reference(tmp_path: Path) -> None:
    create_required_dirs(tmp_path)
    finding = tmp_path / "finding.md"
    finding.write_text(
        """---
artifact_id: FIND-1
artifact_type: finding
client: repository
status: open
sensitivity: INTERNAL
requirement:
  - EX-1
evidence:
  - EVID-MISSING
---
""",
        encoding="utf-8",
    )

    errors = validate(tmp_path)

    assert "dangling evidence reference: EVID-MISSING" in errors

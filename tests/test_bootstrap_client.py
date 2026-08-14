from pathlib import Path

import pytest

from scripts.bootstrap_client import bootstrap_client, validate_client_id


def make_template(root: Path) -> None:
    context = root / "clients" / "_template" / "context"
    context.mkdir(parents=True)
    (context / "project-context.md").write_text(
        "---\nartifact_id: CTX-{{CLIENT_ID}}\nclient: {{CLIENT_ID}}\n"
        "created: {{CREATED_DATE}}\nupdated: {{UPDATED_DATE}}\n---\n",
        encoding="utf-8",
    )


def test_valid_client_creation(tmp_path: Path) -> None:
    make_template(tmp_path)

    destination = bootstrap_client("acme", tmp_path)

    assert destination == tmp_path / "clients" / "acme"
    text = (destination / "context" / "project-context.md").read_text(encoding="utf-8")
    assert "acme" in text
    assert "{{CLIENT_ID}}" not in text


def test_duplicate_client_handling(tmp_path: Path) -> None:
    make_template(tmp_path)
    bootstrap_client("acme", tmp_path)

    with pytest.raises(FileExistsError):
        bootstrap_client("acme", tmp_path)


@pytest.mark.parametrize("client_id", ["Acme", "a", "bad_id", "-bad", "bad-"])
def test_malformed_client_ids(client_id: str) -> None:
    with pytest.raises(ValueError):
        validate_client_id(client_id)

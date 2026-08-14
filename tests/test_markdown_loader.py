from pathlib import Path

from retrieval.loaders.markdown import parse_markdown_file, parse_markdown_text


def test_parse_markdown_front_matter() -> None:
    metadata, body = parse_markdown_text("---\nartifact_id: EVID-1\n---\n# Body\n")

    assert metadata["artifact_id"] == "EVID-1"
    assert body == "# Body\n"


def test_parse_markdown_without_front_matter(tmp_path: Path) -> None:
    path = tmp_path / "note.md"
    path.write_text("# Note\n", encoding="utf-8")

    artifact = parse_markdown_file(path)

    assert artifact.metadata == {}
    assert artifact.body == "# Note\n"

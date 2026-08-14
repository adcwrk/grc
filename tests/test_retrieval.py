from pathlib import Path

from retrieval.search.local import LocalFilesystemRetriever


def write_artifact(path: Path, artifact_id: str, artifact_type: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
artifact_id: {artifact_id}
artifact_type: {artifact_type}
client: acme
status: draft
sensitivity: INTERNAL
tags:
  - identity
---

{body}
""",
        encoding="utf-8",
    )


def test_retrieval_by_keyword(tmp_path: Path) -> None:
    write_artifact(tmp_path / "a.md", "EVID-1", "evidence", "Privileged access review")
    retriever = LocalFilesystemRetriever(tmp_path)

    results = retriever.search("privileged")

    assert [result.artifact_id for result in results] == ["EVID-1"]


def test_retrieval_by_artifact_id(tmp_path: Path) -> None:
    write_artifact(tmp_path / "a.md", "EVID-1", "evidence", "Privileged access review")
    retriever = LocalFilesystemRetriever(tmp_path)

    result = retriever.get_by_artifact_id("EVID-1")

    assert result is not None
    assert result.artifact_type == "evidence"


def test_retrieval_with_metadata_filters(tmp_path: Path) -> None:
    write_artifact(tmp_path / "a.md", "EVID-1", "evidence", "Identity evidence")
    write_artifact(tmp_path / "b.md", "POL-1", "policy", "Identity policy")
    retriever = LocalFilesystemRetriever(tmp_path)

    results = retriever.search("identity", filters={"artifact_type": "policy"})

    assert [result.artifact_id for result in results] == ["POL-1"]

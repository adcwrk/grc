"""Deterministic filesystem-backed retrieval."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from retrieval.loaders.markdown import MarkdownArtifact, parse_markdown_file


class Retriever(ABC):
    """Abstract retrieval interface for current and future backends."""

    @abstractmethod
    def search(
        self,
        query: str,
        filters: dict[str, Any] | None = None,
        limit: int = 10,
    ) -> list[MarkdownArtifact]:
        """Search artifacts using backend-specific ranking."""


class LocalFilesystemRetriever(Retriever):
    """Search Markdown artifacts using metadata, identifiers, and keywords."""

    def __init__(self, root: Path | str = ".") -> None:
        self.root = Path(root).resolve()

    def iter_markdown(self) -> list[Path]:
        ignored = {".git", ".venv", "__pycache__", "node_modules"}
        paths: list[Path] = []
        for path in self.root.rglob("*.md"):
            if any(part in ignored for part in path.parts):
                continue
            paths.append(path)
        return sorted(paths)

    def load_artifacts(self) -> list[MarkdownArtifact]:
        artifacts: list[MarkdownArtifact] = []
        for path in self.iter_markdown():
            try:
                artifacts.append(parse_markdown_file(path))
            except ValueError:
                continue
        return artifacts

    def get_by_artifact_id(self, artifact_id: str) -> MarkdownArtifact | None:
        target = artifact_id.lower()
        for artifact in self.load_artifacts():
            current = artifact.artifact_id
            if current and current.lower() == target:
                return artifact
        return None

    def search(
        self,
        query: str,
        filters: dict[str, Any] | None = None,
        limit: int = 10,
    ) -> list[MarkdownArtifact]:
        filters = filters or {}
        query_terms = [term.lower() for term in query.split() if term.strip()]
        scored: list[tuple[int, MarkdownArtifact]] = []

        for artifact in self.load_artifacts():
            if not _matches_filters(artifact.metadata, filters):
                continue

            searchable = " ".join(
                [
                    artifact.path.as_posix(),
                    artifact.body,
                    " ".join(str(value) for value in artifact.metadata.values()),
                ]
            ).lower()

            score = 0
            artifact_id = artifact.artifact_id
            if artifact_id and query.lower() == artifact_id.lower():
                score += 100
            for term in query_terms:
                if term in searchable:
                    score += searchable.count(term)
            if not query_terms or score > 0:
                scored.append((score, artifact))

        scored.sort(key=lambda item: (-item[0], item[1].path.as_posix()))
        return [artifact for _, artifact in scored[:limit]]


def _matches_filters(metadata: dict[str, Any], filters: dict[str, Any]) -> bool:
    for key, expected in filters.items():
        actual = metadata.get(key)
        if isinstance(actual, list):
            if expected not in actual:
                return False
        elif actual != expected:
            return False
    return True

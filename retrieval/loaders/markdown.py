"""Markdown loading with lightweight YAML front matter support."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class MarkdownArtifact:
    """A Markdown file plus parsed metadata."""

    path: Path
    metadata: dict[str, Any]
    body: str

    @property
    def artifact_id(self) -> str | None:
        value = self.metadata.get("artifact_id")
        return str(value) if value else None

    @property
    def artifact_type(self) -> str | None:
        value = self.metadata.get("artifact_type")
        return str(value) if value else None


def parse_markdown_text(text: str) -> tuple[dict[str, Any], str]:
    """Return parsed front matter and body from Markdown text."""

    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    raw_metadata = text[4:end]
    body = text[end + 5 :]
    loaded = yaml.safe_load(raw_metadata) or {}
    if not isinstance(loaded, dict):
        raise ValueError("YAML front matter must be a mapping")
    return loaded, body


def parse_markdown_file(path: Path) -> MarkdownArtifact:
    """Load a Markdown artifact from disk."""

    text = path.read_text(encoding="utf-8")
    metadata, body = parse_markdown_text(text)
    return MarkdownArtifact(path=path, metadata=metadata, body=body)

#!/usr/bin/env python3
"""Build a machine-readable repository artifact manifest."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from retrieval.loaders.markdown import parse_markdown_file

MANIFEST_PATH = Path(".repository") / "manifest.json"


def build_manifest(root: Path) -> dict[str, Any]:
    artifacts: list[dict[str, Any]] = []
    ignored = {".git", ".venv", "__pycache__", "node_modules"}

    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if any(part in ignored for part in relative.parts):
            continue
        artifact = parse_markdown_file(path)
        metadata = artifact.metadata
        if not metadata.get("artifact_id"):
            continue
        modified_time = _git_modified_time(root, relative) or _filesystem_modified_time(
            path
        )
        artifacts.append(
            {
                "artifact_id": metadata.get("artifact_id"),
                "artifact_type": metadata.get("artifact_type"),
                "path": relative.as_posix(),
                "client": metadata.get("client"),
                "framework": metadata.get("framework", []),
                "requirement": metadata.get("requirement", []),
                "control": metadata.get("control", []),
                "owner": metadata.get("owner"),
                "status": metadata.get("status"),
                "sensitivity": metadata.get("sensitivity"),
                "tags": metadata.get("tags", []),
                "modified_time": modified_time,
            }
        )

    return {
        "manifest_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
    }


def write_manifest(root: Path, output: Path = MANIFEST_PATH) -> Path:
    manifest = build_manifest(root)
    output_path = root / output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_path


def _git_modified_time(root: Path, relative: Path) -> str | None:
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cI", "--", relative.as_posix()],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    value = result.stdout.strip()
    return value or None


def _filesystem_modified_time(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=UTC).isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build .repository/manifest.json.")
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    parser.add_argument("--output", default=MANIFEST_PATH, type=Path)
    args = parser.parse_args()
    output = write_manifest(args.root.resolve(), args.output)
    print(f"Wrote manifest: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

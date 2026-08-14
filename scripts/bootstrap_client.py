#!/usr/bin/env python3
"""Create a client workspace from clients/_template."""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import date
from pathlib import Path

CLIENT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$")


def validate_client_id(client_id: str) -> None:
    if not CLIENT_ID_RE.fullmatch(client_id):
        raise ValueError(
            "Client ID must be 3-64 lowercase letters, numbers, or hyphens; "
            "it must start and end with a letter or number."
        )


def bootstrap_client(client_id: str, root: Path) -> Path:
    validate_client_id(client_id)
    template = root / "clients" / "_template"
    destination = root / "clients" / client_id
    if not template.exists():
        raise FileNotFoundError(f"Missing template workspace: {template}")
    if destination.exists():
        raise FileExistsError(f"Client workspace already exists: {destination}")

    shutil.copytree(template, destination)
    today = date.today().isoformat()
    replacements = {
        "{{CLIENT_ID}}": client_id,
        "{{CREATED_DATE}}": today,
        "{{UPDATED_DATE}}": today,
    }

    for path in destination.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".yml", ".yaml", ".json"}:
            text = path.read_text(encoding="utf-8")
            for old, new in replacements.items():
                text = text.replace(old, new)
            path.write_text(text, encoding="utf-8")

    return destination


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a new GRC client workspace from clients/_template."
    )
    parser.add_argument("client_id", help="Lowercase client identifier, e.g. acme")
    parser.add_argument(
        "--root",
        default=Path.cwd(),
        type=Path,
        help="Repository root. Defaults to current working directory.",
    )
    args = parser.parse_args()

    try:
        destination = bootstrap_client(args.client_id, args.root.resolve())
    except (ValueError, FileExistsError, FileNotFoundError) as exc:
        parser.exit(2, f"error: {exc}\n")

    print(f"Created client workspace: {destination}")
    print("Next steps:")
    print(f"  1. Edit clients/{args.client_id}/context/project-context.md")
    print("  2. Add scope, evidence metadata, and initial tasks")
    print("  3. Run: python scripts/validate_repository.py")
    print("  4. Run: python scripts/build_manifest.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

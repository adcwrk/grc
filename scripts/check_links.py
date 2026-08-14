#!/usr/bin/env python3
"""Check local Markdown links."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.validate_repository import validate


def main() -> int:
    errors = [error for error in validate(Path.cwd()) if "link" in error]
    if errors:
        print("Broken links found:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("No broken local Markdown links found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

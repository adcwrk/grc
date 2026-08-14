#!/usr/bin/env python3
"""Generate a concise client handoff summary from repository state."""

from __future__ import annotations

import argparse
import subprocess
from datetime import date
from pathlib import Path


def _git_recent(root: Path) -> str:
    result = subprocess.run(
        ["git", "log", "--oneline", "-5"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip() or "No committed history yet."


def generate_handoff(root: Path, client_id: str) -> Path:
    context_dir = root / "clients" / client_id / "context"
    if not context_dir.exists():
        raise FileNotFoundError(f"Unknown client context: {context_dir}")

    handoff = context_dir / "handoff.md"
    text = f"""---
artifact_id: HANDOFF-{client_id}
artifact_type: handoff
client: {client_id}
status: draft
sensitivity: INTERNAL
created: {date.today().isoformat()}
updated: {date.today().isoformat()}
tags:
  - handoff
---

# Agent Handoff

## What Are We Doing?

Summarize the active engagement objective from `project-context.md`.

## What Changed Recently?

Recent Git commits:

```text
{_git_recent(root)}
```

## Decisions Made

Read `decisions.md` for durable decisions. Do not infer decisions from chat history.

## Unresolved Items

Read `assumptions.md` and `tasks.md` before continuing work.

## Next Agent Actions

1. Read this file.
2. Read `project-context.md`.
3. Read `decisions.md`, `assumptions.md`, and `tasks.md`.
4. Run `python scripts/validate_repository.py`.
5. Update this handoff after substantial work.

## Read First

- `clients/{client_id}/context/project-context.md`
- `clients/{client_id}/context/decisions.md`
- `clients/{client_id}/context/assumptions.md`
- `clients/{client_id}/context/tasks.md`
- `docs/architecture.md`
- `AGENTS.md`
"""
    handoff.write_text(text, encoding="utf-8")
    return handoff


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate a client handoff file.")
    parser.add_argument("client_id")
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    args = parser.parse_args()
    try:
        output = generate_handoff(args.root.resolve(), args.client_id)
    except FileNotFoundError as exc:
        parser.exit(2, f"error: {exc}\n")
    print(f"Wrote handoff: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

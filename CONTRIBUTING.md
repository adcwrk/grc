# Contributing

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Validation

Run before opening a pull request:

```bash
make validate
make test
make index
```

## GRC Artifact Rules

- Use YAML front matter for retrievable Markdown artifacts.
- Include `artifact_id`, `artifact_type`, `status`, and `sensitivity` where applicable.
- Use synthetic examples in templates.
- Do not commit secrets or unapproved customer evidence.
- Record material decisions in `decisions.md`.
- Update client handoff files after substantial changes.

## Git Workflow

Use feature branches and logical commits. Keep vendor-specific agent files thin and point them back to `AGENTS.md`.

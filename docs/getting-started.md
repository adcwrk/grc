# Getting Started

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Create A Client

```bash
python scripts/bootstrap_client.py acme
```

Then edit:

- `clients/acme/context/project-context.md`
- `clients/acme/context/decisions.md`
- `clients/acme/context/assumptions.md`
- `clients/acme/context/tasks.md`
- `clients/acme/context/handoff.md`

## Build The Manifest

```bash
python scripts/build_manifest.py
```

## Validate

```bash
python scripts/validate_repository.py
pytest
```

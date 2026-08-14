# GRC Knowledge Platform

This repository is a model-agnostic, AI-native GRC operating system. It keeps project memory, evidence metadata, decisions, tasks, and retrieval context in Git so Codex CLI, Claude Code, GitHub Copilot, Cursor, ChatGPT-compatible tools, MCP-compatible agents, and future agents can continue work from the same durable source of truth.

AI conversations are disposable. Repository artifacts are authoritative.

## Architecture

```text
GRC Domain Layer
        ↓
Structured Knowledge
        ↓
Retrieval / Context Layer
        ↓
Agent Adapter Layer
        ↓
Codex / Claude Code / Copilot / Cursor / future agents
        ↓
Git Repository
```

The v1 retrieval layer is deterministic and local: filesystem traversal, Markdown parsing, YAML front matter, exact artifact lookup, metadata filters, and keyword search. Vector databases and semantic search can be added later through adapters without changing the repository memory model.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python scripts/bootstrap_client.py acme
scripts/create-client "Acme Corporation" --engagement-type assessment --framework cmmc
python scripts/build_manifest.py
python scripts/validate_repository.py
pytest
```

For engagement usage, read [docs/consultant-howto.md](docs/consultant-howto.md).

Useful shortcuts:

```bash
make new-client CLIENT=acme
make onboard CLIENT="Acme Corporation"
make index
make validate
make test
make handoff CLIENT=acme
```

## Repository Workflow

1. Create a client workspace with `scripts/create-client "Client Name"` for onboarding, or `python scripts/bootstrap_client.py CLIENT_ID` for a bare template.
2. Fill in `clients/CLIENT_ID/context/project-context.md` before generating policies, assessments, findings, or reports.
3. Put SOW drafts and scope notes in `clients/CLIENT_ID/sow/`.
4. Record material decisions in `decisions.md`.
5. Track assumptions explicitly in `assumptions.md`.
6. Keep `tasks.md` and `handoff.md` current after substantial work.
7. Use YAML front matter on retrievable Markdown artifacts.
8. Run `python scripts/validate_repository.py` and `python scripts/build_manifest.py` before committing.

Consultant workflow details are in [docs/consultant-howto.md](docs/consultant-howto.md).
Client onboarding details are in [docs/CLIENT_ONBOARDING.md](docs/CLIENT_ONBOARDING.md).

## Agent Use

All agents should start with [AGENTS.md](AGENTS.md), then read the relevant client handoff and context files. Vendor-specific instruction files should be thin adapters that point back to `AGENTS.md` to avoid configuration drift.

Compatibility guidance is in [docs/agent-interoperability.md](docs/agent-interoperability.md).

## Security

Use synthetic examples in templates. Do not commit secrets. Do not assume GitHub is approved storage for every evidence artifact, especially regulated or customer-confidential material. Evidence may be represented as metadata that points to an approved external repository.

Sensitivity labels:

- `PUBLIC`
- `INTERNAL`
- `CONFIDENTIAL`
- `CUI`

See [docs/security-model.md](docs/security-model.md) and [docs/data-classification.md](docs/data-classification.md).

## Key Commands

```bash
python scripts/bootstrap_client.py acme
scripts/create-client "Acme Corporation" --source ./intake/acme
scripts/validate-workspace acme
python scripts/build_manifest.py
python scripts/validate_repository.py
python scripts/generate_handoff.py acme
```

The repository manifest is written to `.repository/manifest.json`.

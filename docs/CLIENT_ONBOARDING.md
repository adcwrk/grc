# Client Onboarding

This guide explains how consultants and agentic CLIs should onboard clients into this repository.

## Quick Start

Clone the repository and install development dependencies:

```bash
git clone https://github.com/adcwrk/grc.git
cd grc
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

You can onboard directly with deterministic tooling:

```bash
scripts/create-client "Acme Corporation" \
  --engagement-name "CMMC Level 2 Readiness Assessment" \
  --engagement-type assessment \
  --framework cmmc \
  --framework nist-csf-2.0 \
  --source ./intake/acme \
  --classification CONFIDENTIAL
```

Or launch any capable agentic CLI and use natural language.

## Onboard A Client With Natural Language

Generic agentic CLI:

```text
Onboard Acme Corporation.

This is a CMMC Level 2 readiness assessment mapped to NIST CSF 2.0.
Their documents are located in ./intake/acme.
Set up the workspace, catalog the material, identify missing onboarding information, and prepare the engagement for analysis.
```

Codex CLI:

```text
Use client-onboarding for Acme Corporation. Read agents/client-onboarding.md, use repository scripts for deterministic steps, and persist all engagement state in Git.
```

Claude Code:

```text
Onboard a new client named Acme Corporation using the canonical client onboarding spec. The source material is in ./intake/acme. Do not rely on chat history as the system of record.
```

## What The Agent Should Do

The agent should:

1. Read `AGENTS.md`.
2. Read `agents/client-onboarding.md`.
3. Run `scripts/create-client` with the supplied facts.
4. Review generated onboarding state.
5. Run `scripts/validate-workspace CLIENT_SLUG`.
6. Report facts, assumptions, unresolved questions, source count, and next actions with repository paths.

## Repository Structure

Client onboarding creates or updates:

```text
clients/<client-slug>/
├── client.yaml
├── engagement.yaml
├── context/
├── intake/
├── sources/catalog.jsonl
├── evidence/
├── working/
├── deliverables/
├── decisions/
├── retrieval/
├── onboarding/open-questions.md
├── onboarding/status.yaml
└── logs/activity.jsonl
```

## Resume An Engagement

On another machine or another model:

```bash
git pull --ff-only
scripts/validate-workspace acme
```

Then ask the agent:

```text
What is the current status of the Acme engagement? Reconstruct state from repository files only.
```

The agent should read:

- `clients/acme/client.yaml`
- `clients/acme/engagement.yaml`
- `clients/acme/onboarding/status.yaml`
- `clients/acme/onboarding/open-questions.md`
- `clients/acme/sources/catalog.jsonl`
- `clients/acme/logs/activity.jsonl`
- `clients/acme/context/handoff.md`
- `clients/acme/context/tasks.md`
- `clients/acme/context/decisions.md`

## Security

Do not assume Git is approved storage for all client source documents. `scripts/create-client` catalogs source files by original path and hash; it does not copy or modify them.

Do not commit:

- secrets
- credentials
- API keys
- tokens
- private keys
- unapproved client-confidential files
- regulated evidence that requires local-only handling

Use `classification` values consistently:

- `PUBLIC`
- `INTERNAL`
- `CONFIDENTIAL`
- `CUI`

## Model Portability

This onboarding capability is model-agnostic because:

- `agents/client-onboarding.md` defines the reasoning contract.
- `scripts/create-client` performs deterministic initialization and source cataloging.
- `schemas/*.schema.json` define shared contracts.
- client state is stored in repository files.
- adapter files only point models to the canonical instructions.

Switching from Claude Code to Codex CLI to another agent should not lose engagement state as long as changes are committed and pulled.

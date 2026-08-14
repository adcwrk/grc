# Client Onboarding

This is the canonical, vendor-neutral onboarding specification. Any capable agentic CLI can execute it by reading this file and orchestrating repository scripts.

## Purpose

Initialize or continue a consulting engagement workspace so client context, source provenance, metadata, open questions, audit logs, and retrieval foundations persist in Git.

The repository is the system of record. Conversation history is not.

## Invocation

Treat any of these as onboarding intent:

- "Onboard a new client named Acme Corporation."
- "Onboard Acme for a CMMC readiness assessment."
- "Run onboarding for Acme using files in ./intake/acme."
- "Use client-onboarding."
- "/onboard-client"

Slash commands are optional. The workflow does not depend on slash-command support.

## Inputs

Collect or infer from the user and source material:

- client name
- client slug, if the consultant wants a specific slug
- engagement name
- engagement type
- consultant
- stakeholders
- objectives
- scope
- out-of-scope items
- frameworks
- regulatory requirements
- deliverables
- important dates
- source locations
- known systems
- known business units
- confidentiality and data-handling requirements

Do not ask for information already supplied. Group unresolved questions instead of asking one at a time.

## Deterministic Tools

Use deterministic scripts for deterministic work:

```bash
scripts/create-client "Acme Corporation" \
  --engagement-name "CMMC Level 2 Readiness Assessment" \
  --engagement-type assessment \
  --framework cmmc \
  --framework nist-csf-2.0 \
  --source ./intake/acme \
  --classification CONFIDENTIAL

scripts/validate-workspace acme
python scripts/build_manifest.py
python scripts/validate_repository.py
```

Do not recreate directory creation, ID generation, hashing, cataloging, or validation behavior by ad hoc generated shell commands when scripts exist.

## Workflow

1. Read `AGENTS.md`, this file, `docs/CLIENT_ONBOARDING.md`, and the current repository state.
2. Parse the consultant request for supplied facts.
3. Identify missing onboarding fields as unresolved questions.
4. Run `scripts/create-client` with supplied facts and source paths.
5. Inspect generated files under `clients/<client-slug>/`.
6. Review `clients/<client-slug>/sources/catalog.jsonl`.
7. Review `clients/<client-slug>/onboarding/open-questions.md`.
8. Run `scripts/validate-workspace <client-slug>`.
9. Run repository validation and rebuild the manifest if retrievable artifacts changed.
10. Summarize facts, assumptions, unresolved questions, source count, and next actions with repository paths.

## Expected Outputs

The workspace should contain:

```text
clients/<client-slug>/
├── client.yaml
├── engagement.yaml
├── README.md
├── context/
├── intake/
├── sources/
│   ├── README.md
│   └── catalog.jsonl
├── evidence/
├── working/
├── deliverables/
├── decisions/
├── retrieval/
├── onboarding/
│   ├── open-questions.md
│   └── status.yaml
└── logs/
    └── activity.jsonl
```

## State Management

Persist onboarding state in:

- `clients/<client>/client.yaml`
- `clients/<client>/engagement.yaml`
- `clients/<client>/sources/catalog.jsonl`
- `clients/<client>/onboarding/open-questions.md`
- `clients/<client>/onboarding/status.yaml`
- `clients/<client>/logs/activity.jsonl`
- existing client context files under `clients/<client>/context/`

## Provenance

Every source file must receive a `source_id`, hash, classification, source type, original path, and ingestion timestamp. Never represent an AI-generated assumption as evidence.

Future analytical claims should be traceable:

```text
Finding -> Evidence -> Source -> Original document
```

## Validation Rules

- Client slug must be lowercase letters, numbers, and hyphens.
- Workspace creation must be idempotent.
- Existing client metadata must not be silently overwritten.
- Original source material must not be silently modified.
- Source catalog entries must validate against `schemas/source.schema.json`.
- Client and engagement metadata must validate against their schemas.
- Missing onboarding information must be recorded in open questions.

## Allowed Actions

- Create a new client workspace.
- Continue an existing onboarding run.
- Catalog source files with hashes and metadata.
- Create or update onboarding status.
- Append audit log events.
- Create internal notes and open questions.
- Run validation and tests.

## Human Approval Gates

Ask for explicit consultant approval before:

- deleting client data
- overwriting source material
- changing engagement scope
- finalizing findings
- generating client-facing conclusions
- committing sensitive source documents
- publishing deliverables
- pushing repository changes when the consultant has not already authorized it

Routine local workspace initialization does not require repeated confirmation when the user has requested onboarding.

## Prohibited Actions

- Do not upload client documents to external services automatically.
- Do not commit secrets, credentials, API keys, tokens, or private keys.
- Do not copy restricted framework text into the repository.
- Do not invent client facts.
- Do not treat assumptions as evidence.
- Do not silently overwrite existing client metadata or source catalogs.
- Do not make the workflow depend on a specific LLM, CLI, or vendor API.

## Completion Criteria

Onboarding is minimally complete when:

- workspace exists
- `client.yaml` exists and validates
- `engagement.yaml` exists and validates
- supplied source files are cataloged or explicitly skipped as duplicates
- `open-questions.md` lists unresolved onboarding information
- `status.yaml` records onboarding state
- `activity.jsonl` records important actions
- `scripts/validate-workspace <client>` passes
- the agent reports next actions using repository paths

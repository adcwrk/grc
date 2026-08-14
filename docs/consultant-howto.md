# Consultant How-To

This guide explains how to use the repository correctly during a real GRC engagement. The goal is to make project state portable across computers, consultants, and AI agents without relying on chat history.

For the exact client onboarding procedure, use [ONBOARDING_RUNBOOK.md](ONBOARDING_RUNBOOK.md).

## Core Rule

The repository is the engagement memory. If a fact, decision, assumption, task, evidence record, or assessment note matters, put it in Git.

Do not rely on:

- a prior AI conversation
- a consultant's local notes outside the repository
- an uncommitted working tree
- undocumented verbal decisions

## Engagement Start

Start from a clean `main` branch:

```bash
git switch main
git pull --ff-only
python scripts/bootstrap_client.py CLIENT_ID
```

Use a stable lowercase client ID:

```bash
python scripts/bootstrap_client.py acme
```

For full onboarding with metadata and source cataloging, prefer:

```bash
scripts/create-client "Acme Corporation" \
  --engagement-type assessment \
  --framework cmmc \
  --source ./intake/acme
```

Then complete the initial context files before drafting policies, assessments, findings, or reports:

- `clients/acme/context/project-context.md`
- `clients/acme/context/assumptions.md`
- `clients/acme/context/tasks.md`
- `clients/acme/context/handoff.md`
- `clients/acme/client.yaml`
- `clients/acme/engagement.yaml`
- `clients/acme/sources/catalog.jsonl`
- `clients/acme/onboarding/open-questions.md`
- `clients/acme/sow/`

Minimum useful context:

- customer or engagement identifier
- engagement objective
- applicable frameworks
- systems and environments in scope
- major technologies
- known constraints
- known risks
- current project status
- important references

## Daily Workflow

At the start of a work session:

```bash
git switch main
git pull --ff-only
python scripts/validate_repository.py
```

Read, in order:

1. `AGENTS.md`
2. `clients/CLIENT_ID/context/handoff.md`
3. `clients/CLIENT_ID/context/project-context.md`
4. `clients/CLIENT_ID/context/decisions.md`
5. `clients/CLIENT_ID/context/assumptions.md`
6. `clients/CLIENT_ID/context/tasks.md`

During work:

- Record new facts in the relevant artifact.
- Record uncertain items in `assumptions.md`.
- Record material decisions in `decisions.md`.
- Record follow-up work in `tasks.md`.
- Keep SOW drafts and scope notes in `clients/CLIENT_ID/sow/`.
- Use evidence metadata records instead of pasting sensitive evidence into Git by default.
- Update `handoff.md` after substantial work.

Before ending a work session:

```bash
python scripts/build_manifest.py
python scripts/validate_repository.py
scripts/validate-workspace CLIENT_ID
git status --short
```

Commit coherent changes:

```bash
git add .
git commit -m "docs: update acme engagement context"
git push
```

## Working With AI Agents

Agents can help analyze, draft, map, validate, and curate, but they must work from repository context.

When starting an AI session, instruct the agent to read:

```text
AGENTS.md
README.md
docs/consultant-howto.md
clients/CLIENT_ID/context/handoff.md
clients/CLIENT_ID/context/project-context.md
clients/CLIENT_ID/context/decisions.md
clients/CLIENT_ID/context/assumptions.md
clients/CLIENT_ID/context/tasks.md
```

Require the agent to separate:

- fact
- assumption
- recommendation
- unresolved question

Do not let an agent:

- invent client facts
- silently change assessment conclusions
- accept evidence without provenance
- claim formal assessment results without supporting evidence
- copy restricted framework text into the repository
- commit secrets or unapproved customer data

## Evidence Handling

Create evidence records that describe evidence provenance and location. Do not assume the repository is approved storage for raw customer evidence.

Use external pointers when source evidence must remain in an approved system:

```yaml
evidence_location:
  type: external
  system: approved-document-repository
  reference: EVIDENCE-12345
```

Good evidence metadata should answer:

- What is the evidence?
- Who owns it?
- Which system produced it?
- When was it collected?
- Which scope does it cover?
- Which requirement or control does it support?
- Where is the source artifact stored?
- What is the sensitivity?
- What are the limitations?

## SOW Handling

Use `clients/CLIENT_ID/sow/` for statements of work, change orders, and engagement scope notes.

Use `templates/sow/statement-of-work.md` as the starting point for a new SOW. SOW artifacts should define:

- engagement objectives
- in-scope and out-of-scope work
- applicable frameworks
- deliverables and acceptance criteria
- client responsibilities
- consultant responsibilities
- assumptions and dependencies
- evidence handling expectations
- timeline and change control

Treat SOW content as at least `CONFIDENTIAL` unless approved otherwise. Do not commit signed agreements, pricing, or sensitive contractual terms unless the repository is approved for that data.

## Decisions And Assumptions

Use `decisions.md` for material choices that affect project direction, architecture, scope, assessment interpretation, or deliverables.

Use `assumptions.md` when something is plausible but not verified. An assumption should have a validation path and a status.

Example distinction:

- Fact: `project-context.md` states the identity provider is Entra ID.
- Assumption: MFA is enforced for all privileged users, pending evidence.
- Recommendation: request a conditional access export.
- Unresolved question: whether break-glass accounts are in scope.

## Tasks And Handoff

Use `tasks.md` as the durable backlog. Each task should have an owner, state, priority, dependency, relevant control, and affected artifact where known.

Use `handoff.md` to help the next consultant or AI agent continue. It should say:

- what the engagement is doing
- what changed recently
- what decisions were made
- what remains unresolved
- what the next agent or consultant should do
- which files to read first

Regenerate a draft handoff when useful:

```bash
python scripts/generate_handoff.py CLIENT_ID
```

Review generated handoff content before committing it.

## Validation

Run validation before commits and before telling a client or teammate that repository work is complete:

```bash
python scripts/build_manifest.py
python scripts/validate_repository.py
pytest
```

Validation checks include:

- required repository structure
- invalid metadata
- duplicate artifact IDs
- broken internal links
- unknown client references
- findings without requirement or control references
- dangling evidence references
- evidence records without source pointers

## Git Hygiene

Use small, coherent commits:

```bash
git commit -m "docs: add acme project context"
git commit -m "docs: record acme access control assumptions"
git commit -m "docs: add acme evidence metadata"
```

Prefer pull requests for meaningful engagement changes. Keep generated local files, secrets, and unapproved evidence out of Git.

Before switching computers:

```bash
python scripts/build_manifest.py
python scripts/validate_repository.py
git status --short
git push
```

On the next computer:

```bash
git pull --ff-only
python scripts/validate_repository.py
```

Then read the client handoff first.

## Consultant Checklist

Before client work:

- `main` is current.
- Client workspace exists.
- Project context is filled in.
- Assumptions and tasks are current.

Before using AI:

- Agent has read `AGENTS.md`.
- Agent has read client context and handoff.
- Agent is instructed not to invent client facts.

Before committing:

- Manifest rebuilt.
- Validation passes.
- No secrets or unapproved evidence are staged.
- Handoff updated when project state changed.

Before handing off:

- `handoff.md` explains current status and next steps.
- Open assumptions are explicit.
- Open tasks are current.
- Changes are committed and pushed.

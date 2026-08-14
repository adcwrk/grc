# Repository Agent Instructions

This file is the canonical instruction source for AI coding agents working in this repository. Treat it as authoritative over chat history.

## Required Startup

1. Inspect the repository before changing files.
2. Read this file.
3. Read `README.md`, `docs/architecture.md`, and `docs/operating-model.md`.
4. For client work, read `clients/<client>/context/handoff.md`, `project-context.md`, `decisions.md`, `assumptions.md`, and `tasks.md`.
5. For client onboarding requests, read `agents/client-onboarding.md` and use repository scripts for deterministic steps.
6. Run validation before declaring work complete when tooling changes or GRC artifacts are modified.

## Ground Rules

- Repository artifacts are authoritative. Conversation memory is not.
- Never invent client facts, technologies, systems, assessment results, or evidence.
- Clearly label statements as fact, assumption, recommendation, or unresolved question.
- Cite repository paths when making GRC conclusions.
- Preserve evidence provenance and sensitivity labels.
- Never silently modify assessment conclusions or evidence acceptance status.
- Record material architecture or engagement decisions in the appropriate `decisions.md`.
- Update handoff state after substantial work.
- Validate generated artifacts before declaring completion.
- Prefer portable file formats and open interfaces.
- Do not hard-code the architecture around one LLM vendor or one GRC framework.
- For onboarding, persist state in `client.yaml`, `engagement.yaml`, `sources/catalog.jsonl`, `onboarding/`, and `logs/activity.jsonl`.

## Prohibited Behavior

- Do not copy proprietary framework text into the repository unless the repository already contains a lawful source.
- Do not commit secrets, credentials, access tokens, private keys, or unapproved customer evidence.
- Do not treat assumptions as facts.
- Do not create vendor-specific agent instructions that duplicate or diverge from this file.
- Do not declare formal assessment conclusions without supporting evidence.

## Expected Completion Checklist

- Changed files are scoped to the task.
- Material decisions are recorded.
- Handoff is updated when project state changed.
- `python scripts/validate_repository.py` passes.
- Tests pass when code changed.
- Manifest is rebuilt when retrievable artifacts changed.

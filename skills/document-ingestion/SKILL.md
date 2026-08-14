# Document Ingestion

## Purpose

Classify and catalog supplied consulting source material while preserving original files and provenance.

## Use When

- onboarding a client
- cataloging kickoff notes, policies, procedures, diagrams, spreadsheets, exports, or evidence
- preparing source material for retrieval

## Required Behavior

- Use `scripts/create-client --source PATH` when cataloging onboarding sources.
- Preserve original files.
- Record source IDs, hashes, original paths, classifications, and source types.
- Do not upload source material to external services automatically.

## Output

- `clients/<client>/sources/catalog.jsonl`
- audit entries in `clients/<client>/logs/activity.jsonl`

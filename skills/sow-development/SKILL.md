# SOW Development

## Purpose

Develop statements of work, change orders, and engagement scope documents from durable repository context.

## Use When

- drafting a new SOW
- revising an existing SOW
- converting onboarding information into scope and deliverables
- preparing change orders
- reconciling scope, assumptions, dependencies, and acceptance criteria

## Required Inputs

- `clients/<client>/client.yaml`
- `clients/<client>/engagement.yaml`
- `clients/<client>/context/project-context.md`
- `clients/<client>/context/decisions.md`
- `clients/<client>/context/assumptions.md`
- `clients/<client>/context/tasks.md`
- `clients/<client>/sow/`
- `templates/sow/statement-of-work.md`

## Required Behavior

- Retrieve client and engagement context before drafting.
- Separate facts, assumptions, recommendations, and unresolved questions.
- Cite repository paths or source IDs for scope-sensitive claims.
- Preserve confidentiality and data-handling requirements.
- Keep deliverables tied to acceptance criteria.
- Capture exclusions and dependencies explicitly.
- Route uncertain legal, commercial, pricing, or contracting terms to open questions.

## Output

- draft SOW artifacts under `clients/<client>/sow/`
- change order drafts when scope changes
- open questions for missing SOW inputs
- revision notes identifying changed sections and supporting repository context

## Prohibited Behavior

- Do not invent pricing, legal terms, staffing commitments, dates, or client obligations.
- Do not mark SOWs as executed or accepted without explicit consultant instruction.
- Do not overwrite signed agreements or source material.
- Do not expose sensitive client content beyond approved repository storage.

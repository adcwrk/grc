# Operating Model

## Durable Memory

Every engagement should keep durable state in the client workspace:

- `project-context.md`: engagement facts and scope.
- `decisions.md`: append-friendly decision log.
- `assumptions.md`: assumptions that require validation.
- `tasks.md`: durable backlog.
- `handoff.md`: cross-agent continuation summary.

## Fact Discipline

Agents and humans should separate:

- Fact: supported by repository artifacts or cited external sources.
- Assumption: plausible but not verified.
- Recommendation: proposed action.
- Unresolved question: missing information.

## Change Discipline

Material changes should update:

- relevant artifact metadata
- decision log when architecture or assessment direction changes
- task backlog when work is created or closed
- handoff after substantial work
- manifest after retrievable artifact changes

## Evidence Discipline

Evidence records should preserve provenance, collection date, scope, owner, sensitivity, and storage location. The repository may store metadata without storing the underlying sensitive evidence.

---
artifact_id: TASK-test-client-1-LOG
artifact_type: task
client: "test-client-1"
status: active
sensitivity: INTERNAL
created: "2026-08-13"
updated: "2026-08-13"
tags:
  - tasks
---

# Tasks

| ID | Task | Owner | State | Priority | Dependency | Relevant Control | Affected Artifact |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TASK-0001 | Complete project context | TBD | open | high | none | TBD | project-context.md |
| TASK-0002 | Supply commercial terms for SOW-0001 (fees, rates, payment terms) — OQ-03 | consultant | open | high | none | n/a | sow/SOW-0001-nist-csf-vciso-advisory.md |
| TASK-0003 | Supply engagement dates and term length for SOW-0001 — OQ-04 | consultant | open | high | none | n/a | sow/SOW-0001-nist-csf-vciso-advisory.md |
| TASK-0004 | Define acceptance and signature process for SOW-0001 — OQ-05 | consultant | open | high | none | n/a | sow/SOW-0001-nist-csf-vciso-advisory.md |
| TASK-0005 | Obtain counsel review of legal terms before SOW issuance — OQ-08 | consultant | open | high | TASK-0002 | n/a | sow/SOW-0001-nist-csf-vciso-advisory.md |
| TASK-0006 | Resolve client-of-record name discrepancy — OQ-14 / ASM-0002 | consultant | open | medium | none | n/a | client.yaml |
| TASK-0007 | Name consultant of record in engagement.yaml — OQ-02 | consultant | open | medium | none | n/a | engagement.yaml |

---
artifact_id: ASM-test-client-1-LOG
artifact_type: context
client: "test-client-1"
status: active
sensitivity: INTERNAL
created: "2026-08-13"
updated: "2026-08-13"
tags:
  - assumptions
---

# Assumptions

Track assumptions here so agents do not silently convert them into facts.

| ID | Date | Assumption | Basis | Validation Needed | Status |
| --- | --- | --- | --- | --- | --- |
| ASM-0001 | 2026-08-13 | TBD | TBD | TBD | open |
| ASM-0002 | 2026-08-14 | The client of record is "Apex Precision Components, Inc." as named in intake, not the literal workspace slug `test-client-1`. | `SRC-0003` names the organization; `client.yaml` records the name as `test-client-1`. | Consultant must confirm the legal client name before any SOW is issued. Tracked as OQ-14 in `sow/SOW-0001-nist-csf-vciso-advisory.md`. | open |
| ASM-0003 | 2026-08-14 | All intake material is synthetic AI-generated test data and carries no evidentiary weight. | `SRC-0001`, `SRC-0002`, and `SRC-0003` each declare "Not evidence. Do not use for formal assessment conclusions." | None. This is stated fact in the sources, recorded here so downstream agents do not treat SOW content as validated client fact. | confirmed |
| ASM-0004 | 2026-08-14 | IT and OT environments are separable, so an IT-only scope boundary is workable. | Scope boundary asserted in `SRC-0001` and `SRC-0002`. | `SRC-0002` itself raises whether IT systems are shared with OT networks. Must be verified in discovery. | open |

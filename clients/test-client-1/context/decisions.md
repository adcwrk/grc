---
artifact_id: DEC-test-client-1-LOG
artifact_type: decision
client: "test-client-1"
status: active
sensitivity: INTERNAL
created: "2026-08-13"
updated: "2026-08-13"
tags:
  - decisions
---

# Decisions

Append decisions using this format.

## DEC-0001: Client Source Documents May Be Committed To Git

- Date: 2026-08-13
- Status: accepted
- Issue: Should client source material live in this Git repository, or be cataloged by
  metadata and hash only with documents held outside the repo?
- Decision: Client source documents may be committed to Git for this engagement.
- Rationale: Consultant stated the engagement's highest data sensitivity is `INTERNAL` —
  no CUI, no regulated evidence. `docs/security-model.md` restrictions on regulated and
  customer-confidential material therefore do not bind this material.
- Alternatives considered: metadata-and-hash-only cataloging (repository default in
  `scripts/create-client`); per-document approval.
- Affected artifacts: `clients/test-client-1/engagement.yaml`,
  `clients/test-client-1/sources/catalog.jsonl`, `clients/test-client-1/intake/`.
- Reviewer: consultant (pending named consultant of record).
- Superseded decision: None.
- Constraint: This decision does not extend to secrets, credentials, tokens, private keys,
  CUI, or PII. If any such material enters scope, this decision must be revisited before
  ingestion.

## DEC-0002: Engagement Type And Framework Baseline

- Date: 2026-08-13
- Status: accepted
- Issue: What engagement type and framework(s) govern this workspace?
- Decision: Advisory / vCISO engagement assessed against NIST CSF 2.0 as the sole framework.
- Rationale: Supplied directly by the consultant during onboarding on 2026-08-13.
- Alternatives considered: readiness assessment, formal assessment, gap analysis;
  CMMC Level 2, NIST SP 800-171, ISO 27001.
- Affected artifacts: `clients/test-client-1/engagement.yaml`,
  `clients/test-client-1/frameworks/`.
- Reviewer: consultant (pending named consultant of record).
- Superseded decision: None.

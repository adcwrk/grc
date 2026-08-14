# Metadata Standard

Markdown artifacts should use YAML front matter where practical.

```yaml
---
artifact_id: EVID-0001
artifact_type: evidence
client: example-client
framework:
  - CMMC
requirement:
  - 3.1.1
status: accepted
owner: security-team
source_system: entra-id
sensitivity: CUI
created: 2026-08-13
updated: 2026-08-13
tags:
  - access-control
  - identity
evidence_location:
  type: external
  system: approved-document-repository
  reference: EVIDENCE-12345
---
```

## Common Fields

| Field | Purpose |
| --- | --- |
| `artifact_id` | Stable unique identifier. |
| `artifact_type` | Artifact category such as `evidence`, `finding`, `policy`, `procedure`, `assessment`, `decision`, `task`, `context`, or `handoff`. |
| `client` | Client workspace identifier or `repository`. |
| `framework` | Framework names or short labels. |
| `requirement` | Requirement identifiers. |
| `control` | Control identifiers. |
| `status` | Lifecycle state. |
| `owner` | Accountable owner. |
| `sensitivity` | `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, or `CUI`. |
| `created` | Creation date. |
| `updated` | Last material update date. |
| `tags` | Retrieval tags. |

Metadata should make artifacts retrievable without making Markdown hard to read.

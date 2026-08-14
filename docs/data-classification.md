# Data Classification

Use the `sensitivity` metadata field on retrievable artifacts.

## Labels

| Label | Meaning |
| --- | --- |
| `PUBLIC` | Approved for public release. |
| `INTERNAL` | Internal project material. |
| `CONFIDENTIAL` | Customer, contractual, or business-sensitive material. |
| `CUI` | Controlled Unclassified Information or CUI-related material requiring approved handling. |

## Rules

- Default to `INTERNAL` for templates and synthetic examples.
- Use `CONFIDENTIAL` for customer-specific non-public data.
- Use `CUI` only when the repository and workflow are approved for CUI.
- Store sensitive evidence externally when Git is not approved for the source material.

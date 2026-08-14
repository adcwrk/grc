# Security Model

## Repository Sensitivity

Do not assume GitHub is approved storage for every customer artifact. Store sensitive source evidence outside Git when required and commit only metadata pointers.

## Confidentiality

- Use private repositories for customer engagements unless explicitly approved otherwise.
- Restrict repository access to personnel with a need to know.
- Use branch protection and pull request reviews for regulated work.
- Keep audit-relevant changes in Git history.

## CUI Considerations

Mark CUI artifacts with `sensitivity: CUI`. Before committing CUI, confirm the repository, remote, endpoint devices, and collaborators are approved for CUI handling.

## Secrets

Never commit:

- passwords
- API keys
- access tokens
- private keys
- certificates with private material
- raw exports containing secrets

Use `.env` for local settings and keep it ignored.

## External Evidence

Use `evidence_location` when evidence is stored elsewhere:

```yaml
evidence_location:
  type: external
  system: approved-document-repository
  reference: EVIDENCE-12345
```

## Prohibited Repository Content

- Unapproved customer data.
- Proprietary standards text copied without license.
- Credentials or secrets.
- Raw regulated evidence unless the repository is explicitly authorized.

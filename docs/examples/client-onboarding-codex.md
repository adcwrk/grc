# Codex CLI Example

Prompt:

```text
Use client-onboarding for Acme Corporation.

Engagement: CMMC Level 2 readiness assessment with NIST CSF 2.0 mapping.
Sources: ./intake/acme

Follow agents/client-onboarding.md as authoritative. Use deterministic scripts where available and persist all state to the repository.
```

Expected command orchestration:

```bash
scripts/create-client "Acme Corporation" \
  --engagement-name "CMMC Level 2 Readiness Assessment" \
  --engagement-type assessment \
  --framework cmmc \
  --framework nist-csf-2.0 \
  --source ./intake/acme
scripts/validate-workspace acme
```

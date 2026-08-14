# Generic Agentic CLI Example

Prompt:

```text
Onboard Acme Corporation.

This is a NIST CSF 2.0 and CMMC engagement. I have kickoff notes, policies, architecture diagrams, and evidence in ./intake/acme.

Use agents/client-onboarding.md. Create the workspace, catalog the material, identify missing onboarding information, and prepare the engagement for analysis.
```

Expected agent behavior:

- Reads `AGENTS.md`.
- Reads `agents/client-onboarding.md`.
- Runs `scripts/create-client`.
- Runs `scripts/validate-workspace acme`.
- Reports generated paths and unresolved questions.

# Onboarding Runbook

This is the step-by-step procedure a consultant should follow to onboard a client.

## 1. Start Clean

```bash
git switch main
git pull --ff-only
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

If the virtual environment already exists:

```bash
source .venv/bin/activate
```

Confirm the repository validates before adding client work:

```bash
python scripts/validate_repository.py
```

## 2. Stage Intake Material

Put source material in an approved local intake directory. The default local intake directory is ignored by Git:

```text
./intake/<client-slug>/
```

Example:

```text
./intake/acme/
├── kickoff-notes.md
├── access-control-policy.docx
├── network-architecture.png
└── evidence-export.xlsx
```

Do not place regulated, CUI, secret, or contract-sensitive source files in the repository unless the repository is approved for that data. The onboarding tool catalogs source files by path and hash; it does not copy source files into Git.

## 3. Choose The Onboarding Mode

You can onboard with deterministic commands or through an agentic CLI. Both modes use the same repository contract.

Use deterministic commands when the required facts are known.

Use an agentic CLI when you want help interpreting kickoff notes, grouping open questions, or preparing a summary.

## 4. Deterministic Command

Run:

```bash
scripts/create-client "Acme Corporation" \
  --engagement-name "CMMC Level 2 Readiness Assessment" \
  --engagement-type assessment \
  --framework cmmc \
  --framework nist-csf-2.0 \
  --source ./intake/acme \
  --classification CONFIDENTIAL
```

Common options:

```text
--slug acme
--consultant "Jane Consultant"
--framework nist-csf-2.0
--framework cmmc
--source ./intake/acme
--classification INTERNAL|CONFIDENTIAL|CUI|PUBLIC
```

The command is idempotent. If the client already exists, it continues onboarding and skips already cataloged sources with the same path and hash.

## 5. Agentic CLI Prompt

Launch your preferred agentic CLI:

```bash
codex
```

or:

```bash
claude
```

Then use a prompt like:

```text
Onboard Acme Corporation.

This is a CMMC Level 2 readiness assessment mapped to NIST CSF 2.0.
The intake material is in ./intake/acme.

Read AGENTS.md and agents/client-onboarding.md. Use repository scripts for deterministic steps. Persist onboarding state to the repository and do not rely on chat history.
```

The agent should run `scripts/create-client`, inspect the generated state, run validation, and report next actions with repository paths.

## 6. Review Generated Files

After onboarding, inspect:

```text
clients/<client-slug>/client.yaml
clients/<client-slug>/engagement.yaml
clients/<client-slug>/sources/catalog.jsonl
clients/<client-slug>/onboarding/open-questions.md
clients/<client-slug>/onboarding/status.yaml
clients/<client-slug>/logs/activity.jsonl
clients/<client-slug>/context/project-context.md
clients/<client-slug>/context/tasks.md
clients/<client-slug>/context/handoff.md
```

Check that:

- the client name and slug are correct
- engagement name and type are correct
- frameworks are normalized and complete
- source count matches expectations
- source classifications are appropriate
- open questions are accurate
- no source files were copied into Git by mistake

## 7. Answer Onboarding Questions

Edit:

```text
clients/<client-slug>/onboarding/open-questions.md
clients/<client-slug>/engagement.yaml
clients/<client-slug>/context/project-context.md
clients/<client-slug>/context/assumptions.md
clients/<client-slug>/context/tasks.md
```

Record unknowns as assumptions or open questions. Do not let an AI model convert unanswered questions into facts.

## 8. Validate

Run:

```bash
scripts/validate-workspace <client-slug>
python scripts/validate_repository.py
python scripts/build_manifest.py
pytest
```

Expected result:

```text
Workspace validation passed.
Repository validation passed.
```

## 9. Commit

Review changes:

```bash
git status --short
git diff --stat
```

Do not commit `./intake/` files unless explicitly approved. The `.gitignore` excludes root-level `intake/` by default.

Commit durable onboarding state:

```bash
git add clients/<client-slug> .repository/manifest.json
git commit -m "docs: onboard <client-slug> engagement"
git push
```

## 10. Resume Later

On another machine:

```bash
git clone https://github.com/adcwrk/grc.git
cd grc
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
scripts/validate-workspace <client-slug>
```

Then ask any capable agent:

```text
What is the current status of the <client> engagement? Reconstruct the answer from repository files only.
```

The agent should read:

- `clients/<client-slug>/client.yaml`
- `clients/<client-slug>/engagement.yaml`
- `clients/<client-slug>/onboarding/status.yaml`
- `clients/<client-slug>/onboarding/open-questions.md`
- `clients/<client-slug>/sources/catalog.jsonl`
- `clients/<client-slug>/logs/activity.jsonl`
- `clients/<client-slug>/context/handoff.md`
- `clients/<client-slug>/context/tasks.md`
- `clients/<client-slug>/context/decisions.md`

## Human Approval Gates

Get explicit consultant approval before:

- deleting client data
- overwriting source material
- changing engagement scope
- finalizing findings
- generating client-facing conclusions
- committing sensitive source documents
- publishing deliverables
- pushing changes if the consultant has not authorized it

## Troubleshooting

If `scripts/create-client` cannot import `yaml` or `jsonschema`, activate the virtual environment:

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
```

If `scripts/validate-workspace` warns that an original source path is unavailable, the cataloged source path does not exist on the current machine. This can be normal after moving machines; the source ID and hash still preserve provenance from the onboarding machine.

If a client already exists, rerun onboarding with the same client name or `--slug`. Existing source catalog entries are preserved and duplicate files are skipped.

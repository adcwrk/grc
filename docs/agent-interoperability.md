# Agent Interoperability

## Canonical Instructions

`AGENTS.md` is the canonical repository-wide AI instruction file. Tool-specific instruction files should point back to it instead of duplicating policy.

## Codex CLI

Start Codex in the repository root. The agent should read `AGENTS.md`, `README.md`, and the relevant client handoff before making changes.

For client onboarding, the agent should read `agents/client-onboarding.md` and use `scripts/create-client` plus `scripts/validate-workspace`.

## Claude Code

Use the same repository root. If a Claude-specific instruction file is added later, it should be a thin adapter that says to follow `AGENTS.md`.

For client onboarding, `CLAUDE.md` points back to the canonical onboarding contract.

## Gemini CLI

Use the same repository root. `GEMINI.md` points Gemini-compatible workflows back to `AGENTS.md` and `agents/client-onboarding.md`.

## GitHub Copilot

Copilot should use repository files as context. Keep durable state in Markdown and JSON so Copilot Chat can retrieve it from the workspace.

## Cursor

Open the repository root in Cursor. Cursor rules, if added, should reference `AGENTS.md` and avoid duplicating GRC policy.

## Generic MCP-Compatible Agents

Future MCP tools should wrap retrieval capabilities without changing source artifacts. Agents should prefer repository paths and artifact IDs over chat-only references.

## Future CLI Agents

Any future agent should be able to continue by reading:

1. `AGENTS.md`
2. `README.md`
3. `docs/architecture.md`
4. `clients/<client>/context/handoff.md`
5. `clients/<client>/context/project-context.md`
6. `clients/<client>/context/decisions.md`
7. `clients/<client>/context/assumptions.md`
8. `clients/<client>/context/tasks.md`
9. `clients/<client>/client.yaml`
10. `clients/<client>/engagement.yaml`
11. `clients/<client>/onboarding/status.yaml`
12. `clients/<client>/sources/catalog.jsonl`

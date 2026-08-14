# Retrieval Architecture

## Goals

- Deterministic local retrieval in v1.
- No mandatory vector database.
- Open interfaces for future backends.
- Human-readable source artifacts.
- Machine-readable metadata.

## Interface

```python
class Retriever:
    def search(self, query, filters=None, limit=10):
        ...
```

The current implementation is `retrieval.search.local.LocalFilesystemRetriever`.

## Current Capabilities

- Parse Markdown YAML front matter.
- Search by keyword.
- Retrieve by exact `artifact_id`.
- Filter by metadata fields such as `client`, `artifact_type`, `framework`, `status`, and `sensitivity`.
- Build `.repository/manifest.json`.

## Future Adapters

- SQLite FTS for local indexed search.
- PostgreSQL for multi-user deployments.
- pgvector, Qdrant, or Chroma for semantic retrieval.
- External enterprise search for approved evidence repositories.
- MCP server wrappers for agent access.

## MCP Readiness

Future MCP tools should expose stable repository capabilities:

- `search_knowledge`
- `get_client_context`
- `get_requirement`
- `get_evidence`
- `get_findings`
- `get_decisions`
- `get_open_tasks`
- `generate_handoff`

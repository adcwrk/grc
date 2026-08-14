# Retrieval

The retrieval layer provides deterministic local search over repository artifacts.

Current implementation:

- `retrieval.loaders.markdown`: YAML front matter parser.
- `retrieval.search.local`: filesystem retriever.
- `scripts/build_manifest.py`: writes `.repository/manifest.json`.

Future adapters belong in `retrieval/adapters/` and should implement the same `Retriever` interface.

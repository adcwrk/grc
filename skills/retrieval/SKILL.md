# Retrieval

## Purpose

Retrieve repository context deterministically before reasoning.

## Required Behavior

- Prefer repository metadata, source catalogs, manifests, and exact IDs first.
- Use `retrieval.search.local.LocalFilesystemRetriever` for local Markdown retrieval when useful.
- Do not require a vector database for v1 onboarding.

## Output

- cited repository paths
- source IDs
- relevant client context and onboarding state

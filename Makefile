.PHONY: validate test index new-client handoff lint

CLIENT ?= example

validate:
	python scripts/validate_repository.py

test:
	pytest

index:
	python scripts/build_manifest.py

new-client:
	python scripts/bootstrap_client.py $(CLIENT)

handoff:
	python scripts/generate_handoff.py $(CLIENT)

lint:
	ruff check retrieval scripts tests

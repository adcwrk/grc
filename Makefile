.PHONY: validate test index new-client onboard validate-workspace handoff lint

CLIENT ?= example
CLIENT_NAME ?= Example Client

validate:
	python scripts/validate_repository.py

test:
	pytest

index:
	python scripts/build_manifest.py

new-client:
	python scripts/bootstrap_client.py $(CLIENT)

onboard:
	scripts/create-client "$(CLIENT_NAME)"

validate-workspace:
	scripts/validate-workspace $(CLIENT)

handoff:
	python scripts/generate_handoff.py $(CLIENT)

lint:
	ruff check retrieval scripts tests

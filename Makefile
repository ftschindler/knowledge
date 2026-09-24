.PHONY: help bootstrap site serve

PORT_FILE := .serve-port

## Show available targets
help:
	@grep -B1 '^[a-z]' $(MAKEFILE_LIST) | grep '^##' | sed 's/## /  /'

## Install dependencies and pre-commit hooks
bootstrap:
	uv sync
	uv run prek install

## Build the static site into site/
site:
	NO_MKDOCS_2_WARNING=true uv run mkdocs build --strict

## Start the live-reloading dev server
serve: $(PORT_FILE)
	NO_MKDOCS_2_WARNING=true uv run mkdocs serve -a localhost:$$(cat $(PORT_FILE))

# Pick a random port once and reuse it; delete the file to get a new one
$(PORT_FILE):
	awk 'BEGIN { srand(); print 8000 + int(rand() * 1000) }' > $@
	@echo "picked port $$(cat $@) (stored in $@)"

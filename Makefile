.DEFAULT_GOAL:=all
paths = python

.PHONY: install
install:
	pip install -U pip pre-commit pip-tools
	pip install -r python/requirements/all.txt
	pre-commit install

.PHONY: update-lockfiles
update-lockfiles:
	@echo "Updating requirements files using pip-compile"
	pip-compile -q --strip-extras -o python/requirements/lint.txt python/requirements/lint.in
	pip-compile -q --strip-extras -o python/requirements/pyproject.txt pyproject.toml --extra=fastapi
	pip install --dry-run -r python/requirements/all.txt

.PHONY: format
format:
	ruff check --fix-only $(paths)
	ruff format $(paths)

.PHONY: lint
lint:
	ruff check $(paths)
	ruff format --check $(paths)

.PHONY: typecheck
typecheck:
	pyright python/fastui

.PHONY: test
test:
	coverage run -m pytest tests

.PHONY: testcov
testcov: test
	coverage html

.PHONY: dev
dev:
	uvicorn python.demo:app --reload

.PHONY: all
all: testcov lint

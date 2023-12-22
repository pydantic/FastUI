.DEFAULT_GOAL:=all
path = src/python-fastui

.PHONY: install
install:
	pip install -U pip pre-commit pip-tools
	pip install -r $(path)/requirements/all.txt
	pip install -e $(path)
	pre-commit install

.PHONY: update-lockfiles
update-lockfiles:
	@echo "Updating requirements files using pip-compile"
	pip-compile -q --strip-extras -o $(path)/requirements/lint.txt $(path)/requirements/lint.in
	pip-compile -q --strip-extras -o $(path)/requirements/pyproject.txt -c $(path)/requirements/lint.txt $(path)/pyproject.toml --extra=fastapi
	pip-compile -q --strip-extras -o $(path)/requirements/test.txt -c $(path)/requirements/lint.txt -c $(path)/requirements/pyproject.txt $(path)/requirements/test.in
	pip install --dry-run -r $(path)/requirements/all.txt

.PHONY: format
format:
	ruff check --fix-only $(path) demo
	ruff format $(path) demo

.PHONY: lint
lint:
	ruff check $(path) demo
	ruff format --check $(path) demo

.PHONY: typecheck
typecheck:
	pyright

.PHONY: test
test:
	coverage run -m pytest

.PHONY: testcov
testcov: test
	coverage html

.PHONY: typescript-models
typescript-models:
	fastui generate fastui:FastUI src/npm-fastui/src/models.d.ts

.PHONY: dev
dev:
	uvicorn demo:app --reload --reload-dir .

.PHONY: all
all: testcov lint

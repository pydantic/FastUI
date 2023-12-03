.DEFAULT_GOAL:=all
path = packages/python-fastui

.PHONY: install
install:
	pip install -U pip pre-commit pip-tools
	pip install -r $(path)/requirements/all.txt
	pre-commit install

.PHONY: update-lockfiles
update-lockfiles:
	@echo "Updating requirements files using pip-compile"
	pip-compile -q --strip-extras -o $(path)/requirements/lint.txt $(path)/requirements/lint.in
	pip-compile -q --strip-extras -o $(path)/requirements/pyproject.txt pyproject.toml --extra=fastapi
	pip install --dry-run -r $(path)/requirements/all.txt

.PHONY: format
format:
	ruff check --fix-only $(path)
	ruff format $(path)

.PHONY: lint
lint:
	ruff check $(path)
	ruff format --check $(path)

.PHONY: typecheck
typecheck:
	pyright

.PHONY: test
test:
	coverage run -m pytest tests

.PHONY: testcov
testcov: test
	coverage html

.PHONY: dev
dev:
	uvicorn demo:app --reload

.PHONY: all
all: testcov lint

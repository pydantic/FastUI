.DEFAULT_GOAL:=all
path = src/python-fastui

.PHONY: install
install:
	cd src/python-fastui && pdm install
	cd demo && pdm install


.PHONY: install-docs
install-docs:
	pip install -r requirements/docs.txt

# note -- mkdocstrings-typescript and griffe-typedoc are not yet publicly available
# but the following can be added above the pip install -r requirements/docs.txt line in the future
# pip install mkdocstrings-python mkdocstrings-typescript griffe-typedoc

.PHONY: update-lockfiles
update-lockfiles:
	cd src/python-fastui && pdm sync
	cd demo && pdm sync

.PHONY: format
format:
	cd src/python-fastui && pdm run ruff check --fix-only .
	cd demo && pdm run ruff check --fix-only .

.PHONY: lint
lint:
	cd src/python-fastui && pdm run ruff check .

.PHONY: lint-demo
lint-demo:
	cd demo && pdm run ruff check .


.PHONY: typecheck
typecheck:
	cd src/python-fastui && pdm run pyright fastui

.PHONY: typecheck-demo
typecheck-demo:
	cd demo && pdm run pyright src


.PHONY: test
test:
	cd src/python-fastui && pdm run coverage run -m pytest tests

.PHONY: test-demo
test-demo:
	cd demo && pdm run pytest tests

.PHONY: testcov
testcov: test
	cd src/python-fastui && pdm run coverage html

.PHONY: testcov-report
testcov-report:
	cd src/python-fastui && pdm run coverage report --fail-under=80

testcov-xml:
	cd src/python-fastui && pdm run coverage xml

.PHONY: typescript-models
typescript-models:
	fastui generate fastui:FastUI src/npm-fastui/src/models.d.ts

.PHONY: dev
dev:
	uvicorn demo.src:app --reload --reload-dir .

.PHONY: docs
docs:
	mkdocs build

.PHONY: serve
serve:
	mkdocs serve

.PHONY: all
all: testcov lint

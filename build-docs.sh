#!/usr/bin/env bash

set -e
set -x

python3 -V

python3 -m pip install -r ./requirements/docs.txt
pip install --extra-index-url https://pydantic:$PPPR_TOKEN@pppr.pydantic.dev/simple/ mkdocs-material mkdocstrings-python griffe-typedoc mkdocstrings-typescript
npm install
npm install -g typedoc

python3 -m mkdocs build

#!/usr/bin/env bash

set -e
set -x

python3 -V

python3 -m pip install -r ./requirements/docs.txt

python3 -m mkdocs build

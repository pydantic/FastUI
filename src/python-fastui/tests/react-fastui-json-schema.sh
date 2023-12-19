#!/usr/bin/env bash
# must be called via `npm run generate-json-schema`
set -e
set -x

typescript-json-schema \
  --required src/npm-fastui/tsconfig.json \
  -o src/python-fastui/tests/react-fastui-json-schema.json \
  FastProps

npm run prettier -- src/python-fastui/tests/react-fastui-json-schema.json

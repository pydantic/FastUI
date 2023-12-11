#!/usr/bin/env bash
set -e
set -x
# must be called via `npm run generate-json-schema`
typescript-json-schema --required src/npm-fastui/tsconfig.json -o src/python-fastui/tests/react-fastui-json-schema.json FastProps
npm run prettier -- src/python-fastui/tests/react-fastui-json-schema.json

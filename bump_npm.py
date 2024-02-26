#!/usr/bin/env python
from __future__ import annotations

import json
import re
from pathlib import Path


def replace_package_json(package_json: Path, new_version: str, deps: bool = False) -> tuple[Path, str]:
    content = package_json.read_text()
    content, r_count = re.subn(r'"version": *".*?"', f'"version": "{new_version}"', content, count=1)
    assert r_count == 1 , f'Failed to update version in {package_json}, expect replacement count 1, got {r_count}'
    if deps:
        content, r_count = re.subn(r'"(@pydantic/.+?)": *".*?"', fr'"\1": "{new_version}"', content)
        assert r_count == 1, f'Failed to update version in {package_json}, expect replacement count 1, got {r_count}'

    return package_json, content


def main():
    this_dir = Path(__file__).parent
    fastui_package_json = this_dir / 'src/npm-fastui/package.json'
    with fastui_package_json.open() as f:
        old_version = json.load(f)['version']

    rest, patch_version = old_version.rsplit('.', 1)
    new_version = f'{rest}.{int(patch_version) + 1}'
    bootstrap_package_json = this_dir / 'src/npm-fastui-bootstrap/package.json'
    prebuilt_package_json = this_dir / 'src/npm-fastui-prebuilt/package.json'
    to_update: list[tuple[Path, str]] = [
        replace_package_json(fastui_package_json, new_version),
        replace_package_json(bootstrap_package_json, new_version, deps=True),
        replace_package_json(prebuilt_package_json, new_version),
    ]

    python_init = this_dir / 'src/python-fastui/fastui/__init__.py'
    python_content = python_init.read_text()
    python_content, r_count = re.subn(r"(_PREBUILT_VERSION = )'.+'", fr"\1'{new_version}'", python_content)
    assert r_count == 1, f'Failed to update version in {python_init}, expect replacement count 1, got {r_count}'
    to_update.append((python_init, python_content))

    # logic is finished, no update all files
    print(f'Updating files:')
    for package_json, content in to_update:
        print(f'  {package_json.relative_to(this_dir)}')
        package_json.write_text(content)

    print(f"""
Bumped from `{old_version}` to `{new_version}` in {len(to_update)} files.

To publish the new version, run:

> npm --workspaces publish
""")


if __name__ == '__main__':
    main()

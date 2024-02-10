import json
import re
from pathlib import Path


def replace_package_json(package_json: Path, new_version: str, deps: bool = False) -> None:
    content = package_json.read_text()
    content = re.sub(r'"version": *".*?"', f'"version": "{new_version}"', content)
    if deps:
        content = re.sub(r'"(@pydantic/.+?)": *".*?"', fr'"\1": "{new_version}"', content)
    package_json.write_text(content)


def main():
    this_dir = Path(__file__).parent
    fastui_package_json = this_dir / 'src/npm-fastui/package.json'
    with fastui_package_json.open() as f:
        old_version = json.load(f)['version']

    rest, patch_version = old_version.rsplit('.', 1)
    new_version = f'{rest}.{int(patch_version) + 1}'
    replace_package_json(fastui_package_json, new_version)
    bootstrap_package_json = this_dir / 'src/npm-fastui-bootstrap/package.json'
    replace_package_json(bootstrap_package_json, new_version, deps=True)
    prebuilt_package_json = this_dir / 'src/npm-fastui-prebuilt/package.json'
    replace_package_json(prebuilt_package_json, new_version, deps=True)

    python_init = this_dir / 'src/python-fastui/fastui/__init__.py'
    python_content = python_init.read_text()
    python_content = re.sub(r"(_PREBUILT_VERSION = )'.+'", fr"\1'{new_version}'", python_content)
    python_init.write_text(python_content)

    files = fastui_package_json, bootstrap_package_json, prebuilt_package_json, python_init
    files = '\n'.join(str(f.relative_to(this_dir)) for f in files)
    print(f"""\
Updated version from `{old_version}` to `{new_version}` in:

{files}

To publish the new version, run:

    npm --workspaces publish
""")


if __name__ == '__main__':
    main()
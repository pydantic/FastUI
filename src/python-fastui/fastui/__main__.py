import argparse
from pathlib import Path

from . import __version__, generate_typescript


def cli():
    parser = argparse.ArgumentParser(prog='FastUI', description='FastUI CLI.')
    parser.add_argument(
        '--version',
        action='version',
        version=f'fastui {__version__}',
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    generate_typescript_parser = subparsers.add_parser(
        'generate', help='Generate typescript types from Python definitions of FastUI components.'
    )
    generate_typescript_parser.add_argument(
        'python_object', metavar='python-object', type=str, help='Python object to generate types for.'
    )
    generate_typescript_parser.add_argument(
        'typescript_output_file', metavar='typescript-output-file', type=Path, help='Path to output typescript file.'
    )

    args = parser.parse_args()
    generate_typescript.main(args.python_object, args.typescript_output_file)


if __name__ == '__main__':
    cli()

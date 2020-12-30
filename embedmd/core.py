"""
CLI for embedding markdown within HTML and markdown within markdown
"""

import argparse
import sys

from .html import process_html
from .md import process_markdown


def parse_args():
    parser = argparse.ArgumentParser(
        prog='embedmd',
        description='cli for embedding markdown and html documents into each other',
        usage="embedmd input_file.md -o output_file.md"
    )

    parser.add_argument(
        'input',
        type=str,
        metavar='input',
        help='input filename'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        metavar='file',
        help='optional filename to write to',
    )

    args = parser.parse_args()
    return args


def embedmd():
    args = parse_args()
    input_filename = args.input

    if input_filename.endswith('.html'):
        output = process_html(input_filename)

    elif input_filename.endswith('.md'):
        output = process_markdown(input_filename)

    else:
        print('Can not read input file type', file=sys.stderr)
        quit(-1)

    print(output, file=sys.stdout)

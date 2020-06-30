"""
topo2geo/core.py
"""

import os
import json
from itertools import chain

import click

from . import version as VERSION

CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help']
}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('html_file')
@click.argument('markdown_file')
def main(html_file, markdown_file):
    """
    Embed markdown files into html files
    """
    ...

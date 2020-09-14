
import re
from pathlib import Path
import markdown
import click

from . import html
from . import md

@click.command()
@click.argument('file_path', required=True)
def embedmd(file_path):
    """embedmd is a command line tool for embedding markdown files into other files"""

    if file_path:
        if file_path.endswith('.html'):
            processed_html = html.process_html(file_path)
            print(processed_html)
        elif file_path.endswith('.md'):
            processed_md = md.process_md(file_path)
            print(processed_md)

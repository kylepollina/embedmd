"""embedmd is a command line tool to embed markdown in html

Usage
  embedmd input.html

To embed markdown into your HTML document, add this statement
into your HTML file to link a markdown document:

<#INCLUDE filename.md>

The filename is relative to the HTML file path.You can include
multiple markdown files. You may also add parameters like so:

<#INCLUDE filename.md: param1=hello, param2=world>

Within your markdown file you can define the parameters using
double curly brackets:

{{param1}} {{ param2 }}

These parameters will get replaced with the values you give them"""

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

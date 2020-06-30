"""
topo2geo/core.py
"""

import re
import markdown
from pathlib import Path
import click
from . import version as VERSION

CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help']
}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('html_file')
@click.argument('output_file', required=False)
def embedmd(html_file: str, output_file:str=None):
    """
    Embed markdown files into html files
    """
    if not Path(html_file).exists():
        print(f'Error: file {html_file} does not exist')
        return

    try:
        with open(html_file, 'r') as f:
            html = f.read()
    except:
        print('Error: Could not read file')
        return

    markdown_files = re.findall(r'#INCLUDE (.*).md', html)
    for filename in markdown_files:
        try:
            with open(f'{filename}.md', 'r') as f:
                md = f.read()
        except IOError:
            ...
            continue

        md_html = markdown.markdown(md, extensions=['md_in_html'])
        a = f"'#INCLUDE {filename}.md'"
        print(a)
        html = html.replace(a, md_html)

    output_file = output_file if output_file else html_file

    with open(output_file, 'w+') as f:
        f.write(html)

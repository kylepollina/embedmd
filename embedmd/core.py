"""
embedmd/core.py
"""

import re
from pathlib import Path
import markdown
import click

CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help']
}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('html_file')
def embedmd(html_file):
    """
    Embed markdown files into html files

    within an HTML file, place a link to a markdown file like this:

      '#INCLUDE filename.md'

    and run

      embedmd input.html
    """
    if not Path(html_file).exists():
        print(f'Error: file {html_file} does not exist')
        return

    try:
        with open(html_file, 'r') as f:
            html = f.read()
    except IOError:
        print('Error: Could not read file')
        return

    markdown_files = re.findall(r'#INCLUDE (.*).md', html)
    for filename in markdown_files:
        try:
            with open(Path(html_file).parent / f'{filename}.md', 'r') as f:
                md = f.read()
        except IOError:
            print(f'Error: Filename {filename}.md can not be read. Exiting...')
            quit()

        md_html = markdown.markdown(md, extensions=['extra'])
        search_string = f"'#INCLUDE {filename}.md'"
        html = html.replace(search_string, md_html)

    print(html)

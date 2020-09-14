
from pathlib import Path
import click

from . import html
from . import md


@click.command()
@click.argument('file_path', required=True)
@click.option('--to-html', default=False, is_flag=True, help="""
If --to-html flag added while processing, Markdown document will automatically
be converted to HTML document.

    Ex: embedmd input.md --to-html > output.html
""")
def embedmd(file_path, to_html):
    """embedmd is a command line tool for embedding markdown files into other files"""

    if file_path:
        if file_path.endswith('.html'):
            processed_html = html.process_html(file_path)
            print(processed_html)
        elif file_path.endswith('.md'):
            if to_html:
                print(html.process_html_text(Path('.'), f'<#INCLUDE "{file_path}">'))
            else:
                print(processed_md)

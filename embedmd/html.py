"""
HTML processing
"""

import re
from pathlib import Path

import markdown

from . import md


def process_html(html_filepath: str) -> str:
    """ Processes HTML file and returns the file as a string"""
    html_filepath = Path(html_filepath)

    if not html_filepath.exists():
        print(f'Error: file {html_filepath} does not exist')
        quit(-1)

    try:
        with open(html_filepath, 'r') as f:
            html_text = f.read()

    except IOError:
        print(f'Error reading file {html_filepath}')
        quit(-1)

    included_regex = r'(?P<statement><#include .*\.(md|html)\s*>)'
    included_statements = re.findall(included_regex, html_text, flags=re.IGNORECASE)
    included_statements = [match[0] for match in included_statements]

    for statement in included_statements:
        match = re.search(r'<#include (?P<filename>.*\.(md|html))\s*>', statement, flags=re.IGNORECASE)
        if not match:
            continue
        filename = match.group('filename')
        filepath = html_filepath.parent.absolute() / filename

        if filename.endswith('.html'):
            with open(filepath, 'r') as f:
                tmp_text = f.read()
            html_text = html_text.replace(statement, tmp_text)

        elif filename.endswith('md'):
            md_text = md.process_markdown(filepath)
            html_text = html_text.replace(statement, markdown.markdown(md_text, extensions=['extra']))

    return html_text

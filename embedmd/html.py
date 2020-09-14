"""
HTML processing
"""

import re
from pathlib import Path

import markdown

from . import md


def process_html(html_file_path: str) -> str:
    """ Processes HTML file and returns the file as a string"""
    html_file_path = Path(html_file_path)

    if not html_file_path.exists():
        print(f'Error: file {html_file_path} does not exist')
        quit()

    try:
        with open(html_file_path, 'r') as f:
            html_text = f.read()

    except IOError:
        print(f'Error reading file {html_file_path}')
        quit()

    return process_html_text(html_file_path, html_text)

def process_html_text(html_file_path: Path, html_text: str) -> str:
    """
    Ex:
    included_statements == ['<#INCLUDE file1.md : param1='str', param2=True>', '...']
    """

    for statement in get_included_markdown_statements(html_text):
        # TODO validate statement
        md_filename = get_filename_from_statement(statement)
        md_file_path = html_file_path.parent / md_filename

        md_text = md.process_md(md_file_path)
        html_text = html_text.replace(statement, markdown.markdown(md_text, extensions=['extra']))

    return html_text


def get_included_markdown_statements(text) -> list:
    return re.findall(r'<#INCLUDE "(?:.*?).md(?:.*?)">', text)


def get_filename_from_statement(statement: str) -> str:
    """
    Get the markdown filename from the statement
    """
    filename = re.findall(r'\s"(.*?).md"', statement)
    if len(filename) > 1:
        # Multiple files given in single statement
        raise InvalidStatement(statement)
    filename = filename[0] + '.md'
    filename = filename.strip()
    return filename

class InvalidStatement(Exception):
    pass

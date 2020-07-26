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

    processed_html = process_html(html)
    print(processed_html)

def process_html(html) -> str:
    """
    """

    # Ex:
    # included_statements = ['<#INCLUDE file1.md : param1='str', param2=True>', '...']
    included_statements = get_included_statements(html)

    for statement in included_statements:
        try:
            validate_statement(statement)

            filename = get_filename(statement)
            parameters = get_parameters(statement)
            markdown = process_markdown(filename, parameters)
            html_md = markdown_to_html(markdown)
            html = html.replace(statement, html_md)

        except InvalidStatement:
            ...

    return html


class InvalidStatement(Exception):
    pass

def validate_statement(statement) -> None:
    ...

def process_markdown(filename, parameters):
    ...

def markdown_to_html(markdown) -> str:
    ...

def get_included_statements(html) -> list:
    return re.findall(r'<#INCLUDE (?:.*)>', html)


def get_filename(statement) -> str:
   filename = re.findall(r'\s(.*).md', statement)
   if len(filename) > 1:
       raise InvalidStatement
   filename = filename[0] + '.md'
   filename = filename.strip()
   return filename


def get_parameters(statement) -> list:
    parameters = statement.split(':')

    if len(parameters) == 1:
        return None

    parameters = parameters[1].split(',')
    parameters = [param.strip().replace(' ', '') for param in parameters]
    return parameters

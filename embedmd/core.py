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
    processed_html = process_html(html_file)
    print(processed_html)

def process_html(html_file) -> str:
    """
    TODO
    """

    html_file_path = Path(html_file)

    if not html_file_path.exists():
        print(f'Error: file {html_file} does not exist')
        quit()

    try:
        with open(html_file_path, 'r') as f:
            html = f.read()

    except IOError:
        print(f'Error reading file {html_file}')
        quit()

    """
    Ex:
    included_statements = [
        '<#INCLUDE file1.md : param1='str', param2=True>', '...']
    """
    included_statements = get_included_statements(html)

    for statement in included_statements:
        try:
            validate_statement(statement)

            md_filename = get_filename(statement)
            md_file_path = html_file_path.parent / md_filename
            parameters = get_parameters(statement)

            with open(md_file_path, 'r') as f:
                md = f.read()

            if parameters:
                md = process_markdown(md, parameters)

            html = html.replace(statement, markdown.markdown(md, extensions=['extra']))

        except InvalidStatement:
            ...

        except IOError:
            print(f'Error reading filename {md_filename}')
            quit()

    return html


def validate_statement(statement):
    ...

class InvalidStatement(Exception):
    pass

def process_markdown(md, parameters) -> str:
    for parameter in parameters:
        param_name, param_value = parameter.split('=')
        md = re.sub(
            r'{{(?:\s*)' + param_name + r'(?:\s*)}}',
            param_value,
            md
        )
    return md

def get_included_statements(html) -> list:
    return re.findall(r'<#INCLUDE (?:.*)>', html)


def get_filename(statement) -> str:
    filename = re.findall(r'\s(.*).md', statement)
    if len(filename) > 1:
        raise InvalidStatement
    filename = filename[0] + '.md'
    filename = filename.strip()
    return filename


def get_parameters(statement) -> list or None:
    parameters = statement.split(':')

    if len(parameters) == 1:
        return None

    parameters = parameters[1].split('>')[0].split(',')
    parameters = [param.strip().replace(' ', '') for param in parameters]
    return parameters

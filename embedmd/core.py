"""
embedmd/core.py
"""

import re
from pathlib import Path
import markdown
import click

def print_help(ctx, param):
    msg = """Usage:
  embedmd input.html

Run --help for more help"""
    print(msg)

def print_more_help(ctx):
    print("""embedmd is a command line tool to embed markdown in html

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

These parameters will get replaced with the values you give them""")

@click.command()
@click.argument('html_file', required=False)
@click.option('-h', is_flag=True, expose_value=False)
def embedmd(html_file):
    if html_file:
        processed_html = process_html(html_file)
        print(processed_html)


embedmd.get_help = print_more_help


def process_html(html_file) -> str:
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
            md_filename = get_filename(statement)
            md_file_path = html_file_path.parent / md_filename
            parameters = get_parameters(statement)

            with open(md_file_path, 'r') as f:
                md = f.read()

            if parameters:
                md = process_markdown(md, parameters)

            html = html.replace(statement, markdown.markdown(md, extensions=['extra']))

        except InvalidStatement as e:
            breakpoint()
            print(f'Error invalid statement - {e}')

        except IOError:
            print(f'Error reading filename {md_filename}')
            quit()

    return html


class InvalidStatement(Exception):
    pass


def process_markdown(md, parameters) -> str:
    """
    :param md: text of the markdown file
    :param parameters: list of parameters in the format
                       ['param1=val1', 'param2=val2']
    """

    for parameter in parameters:
        param_name, param_value = parameter.split('=')
        md = re.sub(
            r'{{(?:\s*)' + param_name + r'(?:\s*)}}',
            param_value,
            md
        )
    return md


def get_included_statements(html) -> list:
    return re.findall(r'<#INCLUDE (?:.*?).md(?:.*?)>', html)


def get_filename(statement) -> str:
    """
    Get the markdown filename from the statement
    """
    filename = re.findall(r'\s(.*?).md', statement)
    if len(filename) > 1:
        # Multiple files given in single statement
        raise InvalidStatement(statement)
    filename = filename[0] + '.md'
    filename = filename.strip()
    return filename


def get_parameters(statement) -> list or None:
    """
    Extract the parameters from a statement, if any exist
    """
    parameters = statement.split(':')

    if len(parameters) == 1:
        # No parameters present
        return None
    elif len(parameters) > 2:
        # There should not be more that one : in the statement
        raise InvalidStatement(statement)

    parameters = re.findall(r'<#INCLUDE(?:.*):(.*)>', statement)[0]
    parameters = parameters.strip()

    if len(parameters.split('=')) != len(parameters.split(',')) + 1:
        breakpoint()
        raise InvalidStatement(statement)

    parameters = [param.strip() for param in parameters.split(',')]
    return parameters

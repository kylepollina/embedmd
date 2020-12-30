"""
Markdown processing
"""

from pathlib import Path
import re
import sys

def process_markdown(md_file_path: str) -> str:
    """ Process Markdown file and return the text as a string """
    md_file_path = Path(md_file_path)
    try:
        with open(md_file_path, 'r') as f:
            md_text = f.read()

    except IOError:
        print(f'Error reading file {md_file_path}', file=sys.stderr)
        quit(-1)

    include_regex = r'\[#include (?P<filename>.*\.md)\]'

    for line in md_text.split('\n'):
        match = re.search(include_regex, line, flags=re.IGNORECASE)
        if match:
            included_filename = match.group('filename')
            included_file_path = md_file_path.parent / included_filename

            try:
                with open(included_file_path, 'r') as f:
                    included_md_file_text = f.read()
            except IOError:
                print(f'Error reading file {included_file_path}', file=sys.stderr)
                quit(-1)

            md_text = md_text.replace(line, included_md_file_text)

    return md_text

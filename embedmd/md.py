"""
Markdown processing
"""

from pathlib import Path
import re

def process_md(md_file_path: str) -> str:
    """ Process Markdown file and return the text as a string """
    md_file_path = Path(md_file_path)
    try:
        with open(md_file_path, 'r') as f:
            md_text = f.read()

    except IOError:
        print(f'Error reading file {md_file_path}')
        quit()

    for line in md_text.split('\n'):
        """ TODO documentation """
        if re.match(r'#include ".+\.md"', line):
            included_filename = re.findall(r'".+\.md"', line)[0].strip('"')
            included_file_path = md_file_path.parent / included_filename

            try:
                with open(included_file_path, 'r') as f:
                    included_md_file_text = f.read()
            except IOError:
                print(f'Error reading file {included_md_file_path}')
                quit()

            md_text = md_text.replace(line, included_md_file_text)

    return md_text

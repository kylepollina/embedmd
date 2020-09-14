
import pytest

from embedmd import md

@pytest.mark.parametrize(
    'md_file_path, expected_processed_md',
    [
        ('tests/data/include_other_markdown.md', """hello world\n\nhello world\n""")
    ]
)
def test_process_md(md_file_path, expected_processed_md):
    processed_md = md.process_md(md_file_path)
    assert processed_md == expected_processed_md

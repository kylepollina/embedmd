
import pytest
from embedmd import html


@pytest.mark.parametrize(
    'input_html, expected_statements',
    [
        ('<#INCLUDE "test.md">', ['<#INCLUDE "test.md">']),
        ('<#INCLUDE "test.md">\n<#INCLUDE "test2.md">', ['<#INCLUDE "test.md">', '<#INCLUDE "test2.md">']),
        (
            """
            <p>This paragraph should not be captured</p>
            <h1>Nor should this header</h1>
            <#INCLUDE "test.md">
            <a href='link'>or this link</a>
            <#INCLUDE "test.md">
            """, ['<#INCLUDE "test.md">', '<#INCLUDE "test.md">']
        ),
        ('<#INC<#INCLUDE "test.md">LUDE>', ['<#INCLUDE "test.md">']),
        # Bad inputs
        ('<#INCLUDE test.md>', []),
        ('<#INCLUDE test.md<', []),
        ('#INCLUDE test.md>', []),
        ('<#INCLUDE:>', [])
    ]
)
def test_get_included_markdown_statements(input_html, expected_statements):
    result = html.get_included_markdown_statements(input_html)
    assert result == expected_statements


class TestGetFilenameFromStatement:
    @pytest.mark.parametrize(
        'statement, expected_filename', [
            ("<#INCLUDE test.md>", "test.md"),
            ("<#INCLUDE  test.md>", "test.md")])
    def test_get_filename_from_statement(self, statement, expected_filename):
        assert html.get_filename_from_statement(statement) == expected_filename

    @pytest.mark.parametrize(
        'statement', [
            ("<#INCLUDE test1.md test2.md>")]
    )
    def test_get_filename_from_statement_invalid(self, statement):
        try:
            html.get_filename_from_statement(statement)
            assert False
        except html.InvalidStatement:
            assert True

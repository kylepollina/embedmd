
import pytest
from embedmd import core


@pytest.mark.parametrize(
    'input_html, expected_statements',
    [
        ("<#INCLUDE test.md>", ["<#INCLUDE test.md>"]),
        ("<#INCLUDE test.md>\n<#INCLUDE test2.md>", ["<#INCLUDE test.md>", "<#INCLUDE test2.md>"]),
        (
            """
            <p>This paragraph should not be captured</p>
            <h1>Nor should this header</h1>
            <#INCLUDE test.md>
            <a href="link">or this link</a>
            <#INCLUDE test.md : param1=True, param2='test'>
            """,
            ["<#INCLUDE test.md>", "<#INCLUDE test.md : param1=True, param2='test'>"]
        ),
        ("<#INCLUDE test.md<", []),
        ("#INCLUDE test.md>", [])
    ]
)
def test_get_included_statements(input_html, expected_statements):
    assert core.get_included_statements(input_html) == expected_statements


@pytest.mark.parametrize(
    'statement, expected_filename',
    [
        ("<#INCLUDE test.md>", "test.md"),
        ("<#INCLUDE  test.md>", "test.md")
    ]
)
def test_get_filename(statement, expected_filename):
    assert core.get_filename(statement) == expected_filename

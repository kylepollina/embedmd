
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
            """, ["<#INCLUDE test.md>", "<#INCLUDE test.md : param1=True, param2='test'>"]
        ),
        ("<#INC<#INCLUDE test.md>LUDE>", ['<#INCLUDE test.md>']), # Yeah sure why not
        # Bad inputs
        ("<#INCLUDE test.md<", []),
        ("#INCLUDE test.md>", []),
        ("<#INCLUDE:>", [])
    ]
)
def test_get_included_statements(input_html, expected_statements):
    assert core.get_included_statements(input_html) == expected_statements


class TestGetFilename:
    @pytest.mark.parametrize(
        'statement, expected_filename', [
        ("<#INCLUDE test.md>", "test.md"),
        ("<#INCLUDE  test.md>", "test.md")])
    def test_get_filename(self, statement, expected_filename):
        assert core.get_filename(statement) == expected_filename

    @pytest.mark.parametrize(
        'statement', [
        ("<#INCLUDE test1.md test2.md>")]
    )
    def test_get_filename_invalid(self, statement):
        try:
            core.get_filename(statement)
            assert False
        except core.InvalidStatement:
            assert True


class TestGetParameters:
    @pytest.mark.parametrize(
        'statement, expected_parameters',
        [
            (
                "<#INCLUDE test.md: param1=True, param2='earthscience'>",
                ["param1=True", "param2='earthscience'"]
            ),
            (
                "<#INCLUDE test.md>", None
            ),
        ]
    )
    def test_get_parameters(self, statement, expected_parameters):
        assert core.get_parameters(statement) == expected_parameters

    @pytest.mark.parametrize(
        'invalid_statement',
        [
            ("<#INCLUDE test.md::>"),
        ]
    )
    def test_get_parameters_invalid(self, invalid_statement):
        try:
            core.get_parameters(invalid_statement)
            assert False
        except core.InvalidStatement:
            assert True


@pytest.mark.parametrize(
    'md, params, expected_output',
    [
        ("{{test}}", ["test=True"], "True"),
        ("{{p1}} {{ p2 }}", ["p1=hello", "p2=world"], "hello world")
    ]
)
def test_process_markdown(md, params, expected_output):
    assert core.process_markdown(md, params) == expected_output


import pytest
from embedmd import core

def test_end_to_end():
    with open('tests/test_output.html', 'r') as f:
        expected = f.read()

    assert core.process_html('tests/test_input.html')

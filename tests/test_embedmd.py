
import subprocess


def test_embedmd():
    result = subprocess.run([
        'embedmd', 'tests/test1/input.html'
    ], capture_output=True).stdout.decode('utf-8')

    assert result == '<p>Hello world!</p>\n<p><a href="https://duckduckgo.com/">Here is a link to duckduckgo</a></p>\n<pre><code>and some code\n</code></pre>\n\n'

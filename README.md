
# embedmd

Note: this project has been stalled. The [markdown in HTML](https://python-markdown.github.io/extensions/md_in_html/) extension of the [Markdown](https://python-markdown.github.io/) package does not have any good feature to embed tables into HTML. That was my main use case.

## Installation

```
git clone https://github.com/kylepollina/embedmd
cd embedmd
python3 setup.py install
```

## Usage

Place this text in your HTML file where you want to embed markdown:

```html
'#INCLUDE filename.md'
```

Where `filename.md` is pointing to the markdown file you wish to embed in that spot of the HTML file.

```shell
[~]$ embedmd input.html optional_output.html
```

`embedmd` supports an optional output file if you wish to not overwrite the original file


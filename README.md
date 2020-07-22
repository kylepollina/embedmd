
# embedmd

`embedmd` is a command line tool to embed Markdown documents within HTML. This plugin utilizes the very powerful [Python-Markdown](https://python-markdown.github.io/) package.

## Installation

```
pip install embedmd
```

or

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

Where `filename.md` is pointing to the markdown file you wish to embed in that spot of the HTML file. Then, run the tool from the command line.

```shell
embedmd input.html
```

`embedmd` supports an optional output file if you wish to not overwrite the original file

```shell
embedmd input.html output.html
```

### Example

Say we have this HTML file...

```html
<!-- template.html -->

<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
  </head>
  <body>
    <div id="container">

      '#INCLUDE test1.md'

      '#INCLUDE test2.md'
      
    </div>
  </body>
</html>
```

... and we want to embed these markdown documents within.

```markdown
# test1.md

Hello world, this is brought to you using [embedmd](https://github.com/kylepollina/embedmd)
```

```markdown
# test2.md

| date       | species
| :-----     | :------- 
| 2020-07-21 | Red-winged blackbird
| 2020-07-21 | Eurasian Tree sparrow
```

Running the `embedmd` command:

```
embedmd template.html
```

will change `template.html` to be

```html
<!-- template.html -->

<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
  </head>
  <body>
    <div id="container">

      <h1>test1.md</h1>
<p>Hello world, this is brought to you using <a href="https://github.com/kylepollina/embedmd">embedmd</a></p>

      <h1>test2.md</h1>
<table>
<thead>
<tr>
<th align="left">date</th>
<th align="left">species</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left">2020-07-21</td>
<td align="left">Red-winged blackbird</td>
</tr>
<tr>
<td align="left">2020-07-21</td>
<td align="left">Eurasian Tree sparrow</td>
</tr>
</tbody>
</table>
      
    </div>
  </body>
</html>
```

![](images/img1.png)

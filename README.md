# inscriptis

[![Build Status](https://www.travis-ci.org/weblyzard/inscriptis.png?branch=master)](https://www.travis-ci.org/weblyzard/inscriptis)

A python based HTML to text conversion library, command line client and Web service with support for nested tables and a subset of CSS.
Please take a look at the [Rendering](https://github.com/weblyzard/inscriptis/blob/master/RENDERING.md) document for a demonstration of inscriptis' conversion quality.

##### Table of Contents
1. [Requirements and installation](#requirements-and-installation)
2. [Command line client](#command-line-client)
3. [Python library](#python-library)
4. [Web service](#flask-web-service)
5. [Fine tuning](#fine-tuning)
6. [Testing, benchmarking and evaluation](#testing-benchmarking-and-evaluation)
7. [Changelog](#changelog)

## Requirements and installation

### Requirements
* Python 3.5+ (preferred) or Python 2.7+
* lxml
* requests

### Installation
``` {.sourceCode .bash}
sudo python3 setup.py install
``` 
## Command line client
The command line client converts text files or text retrieved from Web pages to the
corresponding text representation.


### Command line parameters

``` {.sourceCode .bash}
usage: inscript.py [-h] [-o OUTPUT] [-e ENCODING] [-i] [-l] [-d] input

Converts HTML from file or url to a clean text version

positional arguments:
  input                 Html input either from a file or an url (default:stdin)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file (default:stdout).
  -e ENCODING, --encoding ENCODING
                        Content encoding for files (default:utf-8)
  -i, --display-image-captions
                        Display image captions (default:false).
  -l, --display-link-targets
                        Display link targets (default:false).
  -d, --deduplicate-image-captions
                        Deduplicate image captions (default:false).
```

### Examples

```
# convert the given page to text and output the result to the screen
inscript.py https://www.fhgr.ch

# convert the file to text and save the output to output.txt
inscript.py fhgr.html -o fhgr.txt

# convert the text provided via stdin and save the output to output.txt
echo '<body><p>Make it so!</p>></body>' | inscript.py -o output.txt 
```


## Python library

Embedding inscriptis into your code is easy, as outlined below:

```python
import urllib.request
from inscriptis import get_text

url = "http://www.informationscience.ch"
html = urllib.request.urlopen(url).read().decode('utf-8')

text = get_text(html)

print(text)
```

## Flask Web Service

The Flask Web Service translates HTML pages to the corresponding plain text. 

### Additional Requirements

* python3-flask

### Startup

``` {.sourceCode .bash}
export FLASK_APP="web-service.py"
python3 -m flask run
```

### Usage
The Web services receives the HTML file in the request body and returns the corresponding text. The file's encoding needs to be specified 
in the `Content-Type` header (`UTF-8` in the example below).

``` {.sourceCode .bash}
curl -X POST  -H "Content-Type: text/html; encoding=UTF8" -d @test.html  http://localhost:5000/get_text
```

## Fine tuning

1. more rigorous indentation: call `get_text()` with the parameter `indentation='extended'` to also use indentation for tags such as `<div>` and `<span>` that do not provide indentation in their standard definition. This strategy is the default in inscriptis and many other tools such as lynx. If you do not want extended indentation you can use the parameter `indentation='standard'` instead.

2. Overwrite the default CSS definition: inscriptis uses CSS definitions that are maintained in `inscriptis.css.CSS` for rendering HTML tags. You can override these definitions (and therefore change the rendering) as outlined below:

   ```python
   from inscriptis.css import CSS, HtmlElement
   from inscriptis.html_properties import Display

   # change the rendering of `div` and `span` elements
   CSS['div'] = HtmlElement('div', display=Display.block, padding=2)
   CSS['span'] = HtmlElement('span', prefix=' ', suffix=' ')
   ```
   The following code snippet restores the standard behaviour:
   ```python
   from inscriptis.css import CSS, DEFAULT_CSS

   # restore standard behaviour
   CSS = DEFAULT_CSS.copy()
   ```

## Testing, benchmarking and evaluation

### Unit tests

Test cases concerning the html to text conversion are located in the `tests/html` directory and consist of two files:

 1. `test-name.html` and
 2. `test-name.txt`

the latter one containing the reference text output for the given html file.

### Text conversion output comparison and speed benchmarking
inscriptis offers a small benchmarking script that can compare different HTML to txt convertion approaches.
The script will run the different approaches on a list of URLs, `url_list.txt`, and save the text output into a time stamped folder in `benchmarking/benchmarking_results` for manual comparison.
Additionally the processing speed of every approach per URL is measured and saved in a text file called `speed_comparisons.txt` in the respective time stamped folder.

To run the benchmarking script execute `run_benchmarking.py` from within the folder `benchmarking`.
In `def pipeline()` set the which HTML -> Text algorithms to be executed by modifying
```python
run_lynx = True
run_justext = True
run_html2text = True
run_beautifulsoup = True
run_inscriptis = True
```

In `url_list.txt` the URLs to be parsed can be specified by adding them to the file, one per line with no additional formatting. URLs need to be complete (including http:// or https://)
e.g.
```
http://www.informationscience.ch
https://en.wikipedia.org/wiki/Information_science
...
```

## Changelog

see [Release notes](https://github.com/weblyzard/inscriptis/releases).

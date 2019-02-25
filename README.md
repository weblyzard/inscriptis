# inscriptis

A python based HTML to text converter with support for nested tables and a subset of CSS.
Please take a look at the [Rendering](https://github.com/weblyzard/inscriptis/blob/master/RENDERING.md) document for a demonstration of inscriptis' conversion quality.

## Requirements
* Python 3.4+ (preferred) or Python 2.7+
* lxml
* requests

## Usage

### Command line
The command line client converts text files or text retrieved from Web pages to the
corresponding text representation.

#### Installation

``` {.sourceCode .bash}
sudo python3 setup.py install
``` 

#### Command line parameters

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

#### Examples

```
# convert the given page to text and output the result to the screen
inscript.py http://www.htwchur.ch

# convert the file to text and save the output to output.txt
inscript.py htwchur.html -o htwchur.txt

# convert the text provided via stdin and save the output to output.txt
echo '<body><p>Make it so!</p>></body>' | inscript.py -o htwchur.txt 
```


### Library

```python
import urllib.request
from inscriptis import get_text

url = "http://www.informationscience.ch"
html = urllib.request.urlopen(url).read().decode('utf-8')

text = get_text(html)

print(text)
```

## Unit tests

Test cases concerning the html to text conversion are located in the `tests/html` directory and consist of two files:

 1. `test-name.html` and
 2. `test-name.txt`

the latter one containing the reference text output for the given html file.

## Text convertion output comparison and speed benchmarking
inscriptis offers a small benchmarking script that can compare different HTML to txt convertion approaches.
The script will run the different approaches on a list of URLs, ```url_list.txt```, and save the text output into a time stamped folder in ```benchmarking/benchmarking_results``` for manual comparison.
Additionally the processing speed of every approach per URL is measured and saved in a text file called ```speed_comparisons.txt``` in the respective time stamped folder.

To run the benchmarking script execute ```run_benchmarking.py``` from within the folder ```benchmarking```.
In ```def pipeline()``` set the which HTML -> Text algorithms to be executed by modifying
```python
run_lynx = True
run_justext = True
run_html2text = True
run_beautifulsoup = True
run_inscriptis = True
```

In ```url_list.txt``` the URLs to be parsed can be specified by adding them to the file, one per line with no additional formatting. URLs need to be complete (including http:// or https://)
e.g.
```
http://www.informationscience.ch
https://en.wikipedia.org/wiki/Information_science
...
```

## Flask Web Service

The Flask Web Service translates HTML pages to the corresponding plain text. 

### Requirements

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

## Changelog

see [Release notes](https://github.com/weblyzard/inscriptis/releases).

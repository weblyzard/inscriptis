# inscriptis

A python based HTML to text converter based on SpiffWikiMarkup by Samuel Abel.

### Requirements
* Python 3.x
* BeautifulSoup4
* lxml

### Usage

#### Command line
The command line client converts text files or text retrieved from Web pages to the
corresponding text representation.

***Command line parameters***
```bash
usage: inscriptis.py [-h] [-o OUTPUT] [-e ENCODING] input

Converts HTML from file or url to a clean text version

positional arguments:
  input                 Html input either from a file or an url

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file (default:stdout).
  -e ENCODING, --encoding ENCODING
                        Content encoding for files (default:utf-8)
```

***Examples***
```
# convert the given page to text and output the result to the screen
python3 inscriptis.py http://www.htwchur.ch

# convert the file to text and save the output to output.txt
python3 inscriptis.py htwchur.html -o htwchur.txt
```


#### Library

```python
from inscriptis import get_text_from_url

url = "http://www.informationscience.ch"
text = get_text_from_url(url)

print(text)
```

Get text from html
```python
from inscriptis import get_text_from_html

url = "http://www.informationscience.ch"
html = urllib.request.urlopen(url_input)

text = get_text_from_html(html)

print(text)
```

### Text convertion output comparison and speed benchmarking
inscriptis offers a small benchmarking script that can compare different HTML to txt convertion approaches. 
The script will run the different approaches on a list of URLs, ```url_list.txt```, and save the text output into a time stampped folder in ```benchmarking/benchmarking_results``` for manual comparison.
Additionally the processing speed of every approach per URL is measured and saved in a text file called ```speed_comparisons.txt``` in the respective time stampped folder.

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

# inscriptis

A python based HTML to text converter based on SpiffWikiMarkup by Samuel Abel.

### Requirements
* BeautifulSoup4
* lxml

### Usage

Get text from url
The "http://" prefix must be also entered since urllib will not
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

### Benchmarking
To run the benchmarking script ```run_benchmarking.py``` in ```benchmarking```.
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

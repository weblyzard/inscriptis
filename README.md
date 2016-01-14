# inscriptis

A python based HTML to text converter based on SpiffWikiMarkup by Samuel Abel.

### Requirements
* BeautifulSoup4
* lxml


### Usage

Convert single url
The "http://" prefix must be also entered since urllib will not
```python
from inscriptis import get_cleartext

url = "http://www.informationscience.ch"
clear_text = get_cleartext(url)
print(clear_text)
```

Convert multiple urls
```python
from inscriptis import get_cleartext

urls = ["http://www.informationscience.ch", "http://www.informationswissenschaft.ch"]
clear_texts = []
clear_texts.append(get_cleartext(url) for url in urls)
print(clear_texts)
```

To get the runtime of the script use "get_runtime=True"
```python
from inscriptis import get_cleartext

url = "http://www.informationscience.ch"
clear_text, runtime = get_cleartext(url, get_runtime=True)
print("It took {} seconds to convert the html to cleartext\n".format(runtime))
print(clear_text)
```

# To run the comparison script call the script from the command line without any arguments
>>> $ python3.5 tests

# The module can also be called from the command line
# python3.5 inscriptis.py -i
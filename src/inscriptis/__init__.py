'''
Inscripits parses HTML content and converts it into a text representation.
Among others it provides support for

- nested HTML tables and
- basic Cascade Style Sheets.

Example::

   import urllib.request
   from inscriptis import get_text

   url = 'https://www.fhgr.ch'
   html = urllib.request.urlopen(url).read().decode('utf-8')

   text = get_text(html)

   print(text)

'''

__author__ = 'Albert Weichselbraun, Fabian Odoni'
__author_email__ = 'albert.weichselbraun@fhgr.ch, fabian.odoni@fhgr.ch'
__copyright__ = '2016-2020 Albert Weichselbraun, Fabian Odoni'
__license__ = 'GPL2'
__version__ = '1.1'
__status__ = 'Prototype'


try:
    import re
    from lxml.html import fromstring

    from inscriptis.html_engine import Inscriptis

except ImportError:
    import warnings
    warnings.warn(
        "Missing dependencies - inscriptis has not been properly installed")


RE_STRIP_XML_DECLARATION = re.compile(r'^<\?xml [^>]+?\?>')


def get_text(html_content, config=None):
    '''
    Converts an HTML string to text, optionally including and deduplicating
    image captions, displaying link targets and using either the standard
    or extended indentation strategy.


    Args:
      html_content (str): the HTML string to be converted to text.
      config: An optional ParserConfig object.

    Returns:
      str -- The text representation of the HTML content.
    '''
    html_content = html_content.strip()
    if not html_content:
        return ''

    # strip XML declaration, if necessary
    if html_content.startswith('<?xml '):
        html_content = RE_STRIP_XML_DECLARATION.sub('', html_content, count=1)

    html_tree = fromstring(html_content)
    parser = Inscriptis(html_tree, config)
    return parser.get_text()

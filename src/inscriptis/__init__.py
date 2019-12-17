'''
Inscripits parses HTML content and converts it into a text representation.
Among others it provides support for

- nested HTML tables and
- basic Cascade Style Sheets.

Example::

   import urllib.request
   from inscriptis import get_text

   url = "https://www.fhgr.ch"
   html = urllib.request.urlopen(url).read().decode('utf-8')

   text = get_text(html)

   print(text)

'''

import re
from lxml.html import fromstring

from inscriptis.css import DEFAULT_CSS, HtmlElement
from inscriptis.html_engine import Inscriptis
from inscriptis.html_properties import Display

__author__ = "Albert Weichselbraun, Fabian Odoni"
__copyright__ = "2016-2019 Albert Weichselbraun, Fabian Odoni"
__license__ = "GPL2"
__version__ = "0.0.4.2"
__email__ = "albert.weichselbraun@fhgr.ch, fabian.odoni@fhgr.ch"
__status__ = "Prototype"

RE_STRIP_XML_DECLARATION = re.compile(r'^<\?xml [^>]+?\?>')

CSS_PROFILES = {'standard': DEFAULT_CSS,
                'extended': DEFAULT_CSS.copy()}
CSS_PROFILES['extended']['div'] = HtmlElement('div', display=Display.block,
                                              padding=2)
CSS_PROFILES['extended']['span'] = HtmlElement('span', prefix=' ', suffix=' ')


def get_text(html_content, display_images=False, deduplicate_captions=False,
             display_links=False, indentation='extended'):
    '''
    Converts an HTML string to text, optionally including and deduplicating
    image captions, displaying link targets and using either the standard
    or extended indentation strategy.


    Args:
      html_content (str): the HTML string to be converted to text.
      display_images (bool): whether to include image captions in the output.
      deduplicate_captions (bool): whether to deduplicate image captions.
      display_links (bool): whether to display links in the text version.
      indentation: either 'standard' (solely based on the css) or 'extended'
          which intends divs and adds spaces between span tags. The extended
          indentation strategy (default) usually yields better results for
          later text extraction steps.

    Returns:
      str -- The text representation of the HTML content.
    '''
    html_content = html_content.strip()
    if not html_content:
        return ''

    # select the CSS profile required for the selected indentation strategy.
    if indentation not in CSS_PROFILES:
        raise ValueError("Unsupported indentation profile:", indentation)
    css = CSS_PROFILES[indentation]

    # strip XML declaration, if necessary
    if html_content.startswith('<?xml '):
        html_content = RE_STRIP_XML_DECLARATION.sub('', html_content, count=1)

    html_tree = fromstring(html_content)
    parser = Inscriptis(html_tree,
                        display_images=display_images,
                        deduplicate_captions=deduplicate_captions,
                        display_links=display_links,
                        css=css)
    return parser.get_text()

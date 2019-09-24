
import re
from lxml.html import fromstring

from inscriptis.css import CSS, DEFAULT_CSS, HtmlElement
from inscriptis.html_engine import Inscriptis
from inscriptis.html_properties import Display

__author__ = "Albert Weichselbraun, Fabian Odoni"
__copyright__ = "Copyright (C) 2016-2019 Albert Weichselbraun, Fabian Odoni"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Fabian Odoni"
__email__ = "fabian.odoni@htwchur.ch"
__status__ = "Prototype"

RE_STRIP_XML_DECLARATION = re.compile(r'^<\?xml [^>]+?\?>')

def get_text(html_content, display_images=False, deduplicate_captions=False,
             display_links=False, indentation='standard'):
    '''
    :param html_content: the html string to be converted to text
    :param display_images: whether to display image caption
    :param indentation: either 'standard' (solely based on the css) or 'extended'
        which intends divs and adds spaces between span tags
    '''
    html_content = html_content.strip()
    if not html_content:
        return ''

    global CSS
    if indentation == 'extended':
        CSS['div'] = HtmlElement('div', display=Display.block, padding=2)
        CSS['span'] = HtmlElement('span', prefix=' ', suffix=' ')
    else:
        CSS = DEFAULT_CSS

    # strip XML declaration, if necessary
    if html_content.startswith('<?xml '):
        html_content = RE_STRIP_XML_DECLARATION.sub('', html_content, count=1)

    html_tree = fromstring(html_content)
    parser = Inscriptis(html_tree,
                        display_images=display_images,
                        deduplicate_captions=deduplicate_captions,
                        display_links=display_links)
    return parser.get_text()

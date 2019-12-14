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

def get_text(html_content, display_images=False, deduplicate_captions=False,
             display_links=False, indentation='extended'):
    '''
    Converts an HTML string to text.

    :param html_content: the HTML string to be converted to text.
    :param display_images: whether to display image caption.
    :param deduplicate_captions: whether to deduplicate image captions.
    :param display_links: whether to display links in the text version.
    :param indentation: either 'standard' (solely based on the css) or 'extended'
          which intends divs and adds spaces between span tags
    :returns: str -- The text representation of the HTML content.
    '''
    html_content = html_content.strip()
    if not html_content:
        return ''

    if indentation == 'extended':
        css = DEFAULT_CSS.copy()
        css['div'] = HtmlElement('div', display=Display.block, padding=2)
        css['span'] = HtmlElement('span', prefix=' ', suffix=' ')
    else:
        css = DEFAULT_CSS


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

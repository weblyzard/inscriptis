
from re import compile
from lxml.html import fromstring

from inscriptis.html_engine import Inscriptis

__author__ = "Albert Weichselbraun, Fabian Odoni"
__copyright__ = "Copyright (C) 2016 Albert Weichselbraun, Fabian Odoni"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Fabian Odoni"
__email__ = "fabian.odoni@htwchur.ch"
__status__ = "Prototype"

RE_STRIP_XML_DECLARATION = compile(r'^<\?xml [^>]+?\?>')


def get_text(html_content, display_images=False, deduplicate_captions=False, display_links=False):
    '''
    ::param: html_content
    ::returns:
        a text representation of the html content.
    '''
    html_content = html_content.strip()
    if not html_content:
        return ""

    # strip XML declaration, if necessary
    if html_content.startswith('<?xml '):
        html_content = RE_STRIP_XML_DECLARATION.sub('', html_content, count=1)

    html_tree = fromstring(html_content)
    parser = Inscriptis(html_tree, display_images=display_images, deduplicate_captions=deduplicate_captions, display_links=display_links)
    return parser.get_text()

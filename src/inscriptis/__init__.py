
from lxml.html import fromstring

from inscriptis.html_engine import Inscriptis

def get_text(html_content):
    '''
    ::param: html_content
    ::returns:
        a text representation of the html content.
    '''
    html_tree = fromstring(html_content)
    parser = Inscriptis(html_tree)
    return parser.get_text()

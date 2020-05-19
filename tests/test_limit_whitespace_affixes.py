#!/usr/bin/env python

'''
Tests different HTML to text conversion options.
'''

from inscriptis import get_text
from inscriptis.css_profiles import RELAXED_CSS_PROFILE
from inscriptis.model.config import ParserConfig


def test_display_links():
    html = '''<html>
                 <body>
                   hallo<span>echo</span>
                   <pre>
def <span>hallo</span>():
   print("echo")
                   </pre>
                 </body>
                </html>
            '''
    config = ParserConfig(css=RELAXED_CSS_PROFILE)
    assert get_text(html, config).strip() == \
        'hallo echo\n' \
        '\n' \
        'def hallo():\n' \
        '   print("echo")'



#!/usr/bin/env python
# encoding: utf-8

"""
Tests different white-space handling.
"""

from inscriptis import get_text
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

config = ParserConfig(css=CSS_PROFILES['strict'])


def test_margin_handling():
    html = u'''<body>Hallo
                     <div style="margin-top: 1em; margin-bottom: 1em">Echo
                         <div style="margin-top: 2em">Mecho</div>
                     </div>
                     sei Gott
               </body>'''
    assert get_text(html, config) == u'Hallo\n\nEcho\n\n\nMecho\n\nsei Gott'

    html = u'''<body>Hallo
                     <div style="margin-top: 1em; margin-bottom: 1em">Echo</div>
                         <div style="margin-top: 2em">Mecho</div>
                     sei Gott
               </body>'''
    assert get_text(html, config) == u'Hallo\n\nEcho\n\n\nMecho\nsei Gott'

    html = u'''<body>Hallo
                     <div style="margin-top: 1em; margin-bottom: 1em">
                         <div style="margin-top: 2em">Ehre</div>
                    </div>
                    sei Gott
               </body>'''
    assert get_text(html, config) == u'Hallo\n\n\nEhre\nsei Gott'

#!/usr/bin/env python
# encoding: utf-8

'''
Tests different white-space handling.
'''

from inscriptis import get_text
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

config = ParserConfig(css=CSS_PROFILES['strict'])


def test_white_space():
    html = (u'<body><span style="white-space: normal"><i>1</i>2\n3</span>'
            u'</body>')
    assert get_text(html, config) == u'12 3'

    html = (u'<body><span style="white-space: nowrap"><i>1</i>2\n3</span>'
            u'</body>')
    print(get_text(html))
    assert get_text(html, config) == u'12 3'

    html = (u'<body><span style="white-space: pre"><i>1</i>2\n3</span>'
            u'</body>')
    assert get_text(html, config) == u'12\n3'

    html = (u'<body><span style="white-space: pre-line"><i>1</i>2\n3</span>'
            u'</body>')
    assert get_text(html, config) == u'12\n3'

    html = (u'<body><span style="white-space: pre-wrap"><i>1</i>2\n3</span>'
            u'</body>')
    assert get_text(html, config) == u'12\n3'

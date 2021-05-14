#!/usr/bin/env python

""" ensures that two successive <a>text</a> contain
    a space between each other, if there is a linebreak
    or space between the tags.
"""

from inscriptis import get_text


def test_content():
    html = '<html><body>first</body></html>'
    assert get_text(html) == 'first'


def test_margin_before():
    html = '<html><body><p>first</p></body></html>'
    assert get_text(html) == 'first'

    html = '<html><body>first<p>' \
           'second</p></body></html>'
    assert get_text(html) == 'first\nsecond'


def test_br():
    html = '<html><body><br>' \
           'first</p></body></html>'
    assert get_text(html) == '\nfirst'

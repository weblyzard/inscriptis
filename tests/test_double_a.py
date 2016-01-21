#!/usr/bin/env python

''' ensures that two successive <a>text</a> contain
    a space between each other, if there is a linebreak
    or space between the tags.
'''

from inscriptis import get_text_from_html

def test_successive_a():
    html = u'<html><body><a href="first">first</a><a href="second">second</a></body></html>'
    assert get_text_from_html(html) == 'firstsecond'

    html = u'<html><body><a href="first">first</a>\n<a href="second">second</a></body></html>'
    assert get_text_from_html(html) == 'first second'

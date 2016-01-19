#!/usr/bin/env python

''' ensures that two successive <a>text</a> contain
    a space between each other, if there is a linebreak
    or space between the tags.
'''

from inscriptis import get_text_from_html

def test_successive_a():
    html = u'Thomas<div>Anton</div>Maria'
    assert get_text_from_html(html) == 'Thomas\n\nAnton\n\nMaria'

    html = u'Thomas <ul><li><div>Anton</div>Maria</ul>'
    assert get_text_from_html(html) == 'Thomas\n  * Anton\n    Maria'



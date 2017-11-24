#!/usr/bin/env python

''' ensures that two successive <a>text</a> contain
    a space between each other, if there is a linebreak
    or space between the tags.
'''

from inscriptis.css import CssParse, HtmlElement

def test_style_unit_parsing():
    html_element = CssParse.get_style_attribute("margin-top:2.666666667em;margin-bottom: 2.666666667em", html_element=HtmlElement())
    assert html_element.margin_before == 3
    assert html_element.margin_after == 3


#!/usr/bin/env python

"""
Tests inscriptis' parsing of CSS style definitions.
"""

from inscriptis.model.css import CssParse
from inscriptis.model.html_element import HtmlElement


def test_style_unit_parsing():
    html_element = HtmlElement()
    CssParse.attr_style("margin-top:2.666666667em;margin-bottom: 2.666666667em", html_element)
    assert html_element.margin_before == 3
    assert html_element.margin_after == 3

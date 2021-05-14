#!/usr/bin/env python
# encoding: utf-8

"""
Tests HtmlElement and the parsing of CSS style definitiosn
"""

from copy import copy
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.html_properties import Display, WhiteSpace
from inscriptis.model.css import CssParse, HtmlElement


def test_css_parsing():
    html_element = copy(CSS_PROFILES['strict']['div'])
    CssParse.attr_style('padding_left: 8px; display: block', html_element)
    assert html_element.padding == 1
    assert html_element.display == Display.block

    CssParse.attr_style('margin_before: 8em; display: inline', html_element)
    assert html_element.margin_before == 8
    assert html_element.display == Display.inline


def test_html_element_str():
    '''
    Tests the string representation of an HtmlElement.
    '''
    html_element = HtmlElement('div', '', '', Display.inline, 0, 0, 0,
                               WhiteSpace.pre)
    assert str(html_element) == ('<div prefix=, suffix=, '
                                 'display=Display.inline, margin_before=0, '
                                 'margin_after=0, padding=0, '
                                 'whitespace=WhiteSpace.pre, '
                                 'align=HorizontalAlignment.left, '
                                 'valign=VerticalAlignment.middle>')

#!/usr/bin/env python

"""
Tests HtmlElement and the parsing of CSS style definitiosn
"""

from copy import copy

from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.html_properties import (
    Display,
    HorizontalAlignment,
    VerticalAlignment,
    WhiteSpace,
)
from inscriptis.model.css import CssParse
from inscriptis.model.html_element import HtmlElement


def test_css_parsing():
    html_element = copy(CSS_PROFILES["strict"]["div"])
    CssParse.attr_style("padding_left: 8px; display: block", html_element)
    assert html_element.padding_inline == 1
    assert html_element.display == Display.block

    CssParse.attr_style("margin_before: 8em; display: inline", html_element)
    assert html_element.margin_before == 8
    assert html_element.display == Display.inline


def test_html_element_str():
    """
    Tests the string representation of an HtmlElement.
    """
    html_element = HtmlElement("div", "", "", Display.inline, 0, 0, 0, "", WhiteSpace.pre)
    assert str(html_element) == (
        "<div prefix=, suffix=, "
        "display=Display.inline, margin_before=0, "
        "margin_after=0, padding_inline=0, "
        "list_bullet=, "
        "whitespace=WhiteSpace.pre, "
        "align=HorizontalAlignment.left, "
        "valign=VerticalAlignment.middle, "
        "annotation=()>"
    )


def test_parse_vertical_align():
    html_element = HtmlElement()
    CssParse.attr_vertical_align("top", html_element)
    assert html_element.valign == VerticalAlignment.top

    # invalid value
    CssParse.attr_vertical_align("unknown", html_element)
    assert html_element.valign == VerticalAlignment.top


def test_parse_horizontal_align():
    html_element = HtmlElement()
    CssParse.attr_horizontal_align("center", html_element)
    assert html_element.align == HorizontalAlignment.center

    # invalid value
    CssParse.attr_horizontal_align("unknown", html_element)
    assert html_element.align == HorizontalAlignment.center

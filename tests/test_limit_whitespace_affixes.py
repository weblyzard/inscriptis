#!/usr/bin/env python

"""
Tests different HTML to text conversion options.
"""

from copy import copy

from inscriptis import get_text
from inscriptis.css_profiles import RELAXED_CSS_PROFILE
from inscriptis.html_properties import Display, WhiteSpace
from inscriptis.model.config import ParserConfig
from inscriptis.model.html_element import HtmlElement


def test_html_element_refinement():
    new = HtmlElement(
        "span",
        display=Display.inline,
        prefix=" ",
        suffix=" ",
        limit_whitespace_affixes=True,
    )
    pre = HtmlElement("pre", display=Display.block, whitespace=WhiteSpace.pre)
    code = HtmlElement("code")

    # refinement with pre and whitespaces
    refined = pre.get_refined_html_element(copy(new))
    assert refined.prefix == ""
    assert refined.suffix == ""

    # refinement with code and whitespaces
    refined = code.get_refined_html_element(copy(new))
    assert refined.prefix == " "
    assert refined.suffix == " "

    # refinement with pre and non-whitespaces
    new.prefix = " 1. "
    new.suffix = "<"
    refined = pre.get_refined_html_element(copy(new))
    assert refined.prefix == " 1. "
    assert refined.suffix == "<"

    # refinement with code and non-whitespaces
    refined = code.get_refined_html_element(copy(new))
    assert refined.prefix == " 1. "
    assert refined.suffix == "<"


def test_limit_whitespace_affixes():
    html = """<html>
                 <body>
                   hallo<span>echo</span>
                   <pre>
def <span>hallo</span>():
   print("echo")
                   </pre>
                 </body>
                </html>
            """
    config = ParserConfig(css=RELAXED_CSS_PROFILE)
    assert get_text(html, config).strip() == 'hallo echo\n\ndef hallo():\n   print("echo")'

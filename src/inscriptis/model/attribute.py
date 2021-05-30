#!/usr/bin/env python
# encoding: utf-8

"""
This class handles HTML attributes such as `align`, and `valign` by
mapping them to the corresponding functions in the CssParse class.
"""
from typing import Dict

from inscriptis.model.css import CssParse
from inscriptis.model.html_element import HtmlElement

HTML_ATTRIBUTE_MAPPING = {
    'style': CssParse.attr_style,
    'align': CssParse.attr_horizontal_align,
    'valign': CssParse.attr_vertical_align
}


def apply_attributes(attributes: Dict[str, str], html_element: HtmlElement):
    """
    Applies the attributes to the given HTML element.

    Args:
        attributes: the list of attributes
        html_element: the HTML element for which the attributes are parsed
    """
    supported_attributes = filter(lambda t: t[0] in HTML_ATTRIBUTE_MAPPING,
                                  attributes.items())
    for attr_name, attr_value in supported_attributes:
        HTML_ATTRIBUTE_MAPPING[attr_name](attr_value, html_element)
    return html_element

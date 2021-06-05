#!/usr/bin/env python
# encoding: utf-8

"""
This class handles HTML attributes such as `align`, and `valign` by
mapping them to the corresponding functions in the CssParse class.
"""
from typing import Dict, Callable

from inscriptis.model.css import CssParse
from inscriptis.model.html_element import HtmlElement

ATTRIBUTE_MAP = {
    'style': CssParse.attr_style,
    'align': CssParse.attr_horizontal_align,
    'valign': CssParse.attr_vertical_align
}


class Attribute:
    """
    Applies attributes and annotations to the given HTML element.

    Args
        attribute_mapping: a mapping of attribute to the corresponding CSS
                           parsing functions responsible for parsing it.
        annotations: an optional mapping of attributes to the corresponding
                     annotations.
    """
    def __init__(self, attribute_mapping: Dict[str, Callable] = ATTRIBUTE_MAP,
                 annotations: Dict[str, Callable] = None):
        if annotations:
            attribute_mapping.update(annotations)
        self.attribute_mapping = attribute_mapping

    def apply_attributes(self, attributes: Dict[str, str],
                         html_element: HtmlElement) -> HtmlElement:
        """
        Applies the attributes to the given HTML element.

        Args:
            attributes: the list of attributes
            html_element: the HTML element for which the attributes are parsed
        """
        supported_attributes = ((name, val) for name, val in attributes.items()
                                if name in self.attribute_mapping)
        for attr_name, attr_value in supported_attributes:
            self.attribute_mapping[attr_name](attr_value, html_element)
        return html_element

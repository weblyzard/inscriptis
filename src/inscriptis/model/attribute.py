#!/usr/bin/env python
# encoding: utf-8

"""
This class handles HTML attributes such as `align`, and `valign` by
mapping them to the corresponding functions in the CssParse class.
"""
from copy import copy
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
        annotations: an optional mapping of attributes to the corresponding
                     annotations.

    Note: The current implementation allows annotation attributes to
          override attributes in the ATTRIBUTE_MAP. Given the typical
          separation of attributes referring to layout (e.g., style, etc.) and
          structure (e.g., id, class) this is currently not considered.
    """
    
    def __init__(self, annotations: Dict[str, Callable] = None):
        if annotations:
            self.attribute_mapping = copy(ATTRIBUTE_MAP).update(annotations)
        else:
            self.attribute_mapping = ATTRIBUTE_MAP

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

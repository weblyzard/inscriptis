#!/usr/bin/env python
# encoding: utf-8

"""
This class handles HTML attributes such as `align`, and `valign` by
mapping them to the corresponding functions in the CssParse class.
"""
from copy import copy
from typing import Dict, List

from inscriptis.annotation.parser import ApplyAnnotation
from inscriptis.model.css import CssParse
from inscriptis.model.html_element import HtmlElement

DEFAULT_ATTRIBUTE_MAP = {
    'style': CssParse.attr_style,
    'align': CssParse.attr_horizontal_align,
    'valign': CssParse.attr_vertical_align
}


def merge_function(func1, func2):
    """
    Merges two functions with the same arguments into a single one.

    Args:
        func1: the first function
        func2: the second function
    """
    def merged(*args):
        func1(*args)
        func2(*args)
    return merged


class Attribute:
    """
    Applies attributes and annotations to the given HTML element.

    Args
        annotations: an optional mapping of attributes to the corresponding
                     annotations.
    """
    def __init__(self):
        self.attribute_mapping = DEFAULT_ATTRIBUTE_MAP

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

    def merge_attribute_map(self, annotations: List[ApplyAnnotation] = None):
        attributes = copy(self.attribute_mapping)
        for a in annotations:
            attributes[a.attr] = a.apply if a.attr not in attributes \
                else merge_function(attributes[a.attr], a.apply)
        self.attribute_mapping = attributes

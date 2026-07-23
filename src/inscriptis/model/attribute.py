#!/usr/bin/env python3

"""HTML attribute handling."""

from collections.abc import Callable
from copy import copy

from inscriptis.annotation.parser import ApplyAnnotation
from inscriptis.model.css import CssParse
from inscriptis.model.html_element import HtmlElement

AttributeHandler = Callable[[str, HtmlElement], None]


DEFAULT_ATTRIBUTE_MAP : dict[str, AttributeHandler] = {
    "style": CssParse.attr_style,
    "align": CssParse.attr_horizontal_align,
    "valign": CssParse.attr_vertical_align,
}


def merge_function(func1: AttributeHandler, func2: AttributeHandler) -> AttributeHandler:
    """Merge two functions with the same arguments into a single one.

    This function is used for cascading functions that operate on HtmlElements
    and attributes.

    Args:
        func1: the first function
        func2: the second function

    """

    def merged(*args):
        func1(*args)
        func2(*args)

    return merged


class Attribute:
    """Handle HTML attributes such as `align`, and `valign`.

    This class handles HTML attributes by mapping them to the corresponding
    functions in the :class:`~inscriptis.model.css.CssParse` class.

    Attributes:
        attribute_mapping: a mapping of attributes to the corresponding handler
                           functions.

    """

    def __init__(self):
        self.attribute_mapping: dict[str, AttributeHandler] = DEFAULT_ATTRIBUTE_MAP

    def apply_attributes(self, attributes: dict[str, str], html_element: HtmlElement) -> HtmlElement:
        """Apply the attributes to the given HTML element.

        Args:
            attributes: the list of attributes
            html_element: the HTML element for which the attributes are parsed

        """
        for attr_name, attr_value in attributes.items():
            if attr_name in self.attribute_mapping:
                self.attribute_mapping[attr_name](attr_value, html_element)
        return html_element

    def merge_attribute_map(self, annotations: list[ApplyAnnotation]) -> None:
        attributes = copy(self.attribute_mapping)
        for a in annotations:
            attributes[a.attr] = a.apply if a.attr not in attributes else merge_function(attributes[a.attr], a.apply)
        self.attribute_mapping = attributes

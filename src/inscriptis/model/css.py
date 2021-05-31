#!/usr/bin/env python
# coding: utf-8
"""
This module implements basic CSS support for inscriptis.

- The :class:`HtmlElement` class encapsulates all CSS properties of a single
  HTML element.
- :class:`CssParse` parses CSS specifications and translates them into the
  corresponding HtmlElements used by Inscriptis for rendering HTML pages.
"""
from contextlib import suppress
from re import compile as re_compile
from inscriptis.html_properties import (Display, WhiteSpace,
                                        HorizontalAlignment, VerticalAlignment)


class CssParse:
    """
    Parses CSS specifications and translates them into the corresponding
    HtmlElements.

    The attribute `display: none`, for instance, is translated to
    `HtmlElement.display=Display.none`.
    """
    # used to separate value and unit from each other
    RE_UNIT = re_compile(r'(-?[0-9.]+)(\w+)')

    @staticmethod
    def attr_style(style_attribute, html_element):
        """
        Applies the provided style attributes to the given html_element.

        Args:
          style_attribute: The attribute value of the given style sheet.
                           Example: display: none
          html_element: The HtmlElement to which the given style is applied.
        """
        for style_directive in style_attribute.lower().split(';'):
            if ':' not in style_directive:
                continue
            key, value = (s.strip() for s in style_directive.split(':', 1))

            try:
                apply_style = getattr(CssParse, 'attr_'
                                      + key.replace('-webkit-', '')
                                      .replace('-', '_'))
                apply_style(value, html_element)
            except AttributeError:
                pass

    @staticmethod
    def _get_em(length):
        """
        Args:
          length (str): the length (e.g. 2em, 2px, etc.) as specified in the
                        CSS.

        Returns:
            int -- the length in em's.
        """
        _m = CssParse.RE_UNIT.search(length)
        value = float(_m.group(1))
        unit = _m.group(2)

        if unit not in ('em', 'qem', 'rem'):
            return int(round(value / 8))
        return int(round(value))

    # ------------------------------------------------------------------------
    # css styles
    # ------------------------------------------------------------------------

    @staticmethod
    def attr_display(value, html_element):
        """
        Apply the given display value.
        """
        if html_element.display == Display.none:
            return

        if value == 'block':
            html_element.display = Display.block
        elif value == 'none':
            html_element.display = Display.none
        else:
            html_element.display = Display.inline

    @staticmethod
    def attr_white_space(value, html_element):
        """
        Apply the given white-space value.
        """
        if value in ('normal', 'nowrap'):
            html_element.whitespace = WhiteSpace.normal
        elif value in ('pre', 'pre-line', 'pre-wrap'):
            html_element.whitespace = WhiteSpace.pre

    @staticmethod
    def attr_margin_top(value, html_element):
        """
        Apply the given top margin.
        """
        html_element.margin_before = CssParse._get_em(value)

    @staticmethod
    def attr_margin_bottom(value, html_element):
        """
        Apply the provided bottom margin.
        """
        html_element.margin_after = CssParse._get_em(value)

    @staticmethod
    def attr_padding_left(value, html_element):
        """
        Apply the given left padding_inline.
        """
        html_element.padding_inline = CssParse._get_em(value)

    @staticmethod
    def attr_horizontal_align(value, html_element):
        """
        Apply the provided horizontal alignment.
        """
        with suppress(KeyError):
            html_element.align = HorizontalAlignment[value]

    @staticmethod
    def attr_vertical_align(value, html_element):
        """
        Apply the given vertical alignment.
        """
        with suppress(KeyError):
            html_element.valign = VerticalAlignment[value]

    # register aliases
    attr_margin_before = attr_margin_top
    attr_margin_after = attr_margin_bottom
    attr_padding_start = attr_padding_left

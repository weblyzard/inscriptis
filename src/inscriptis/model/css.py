#!/usr/bin/env python
# coding: utf-8
'''
This module implements basic CSS support for inscriptis.

- The :class:`HtmlElement` class encapsulates all CSS properties of a single
  HTML element.
- :class:`CssParse` parses CSS specifications and translates them into the
  corresponding HtmlElements used by Inscriptis for rendering HTML pages.
'''
from re import compile as re_compile
from inscriptis.html_properties import Display, WhiteSpace


class HtmlElement():
    '''
    The HtmlElement class stores the following CSS propierties of HTML
    elements:

    - tag: tag name of the given HtmlElement.
    - prefix: specifies a prefix that to insert before the tag's content.
    - suffix: a suffix to append after the tag's content.
    - display: :class:`~inscriptis.html_properties.Display` strategy used for
      the content.
    - margin_before: vertical margin before the tag's content.
    - margin_after: vertical margin after the tag's content.
    - padding: horizontal padding before the tag's content.
    - whitespace: the :class:`~inscriptis.html_properties.Whitespace` handling
      strategy.
    - limit_whitespace_affixes: limit printing of whitespace affixes to
      elements with `normal` whitepsace handling.
    '''

    __slots__ = ('tag', 'prefix', 'suffix', 'display', 'margin_before',
                 'margin_after', 'padding', 'whitespace',
                 'limit_whitespace_affixes')

    def __init__(self, tag='/', prefix='', suffix='', display=None,
                 margin_before=0, margin_after=0, padding=0,
                 whitespace=None, limit_whitespace_affixes=False):
        self.tag = tag
        self.prefix = prefix
        self.suffix = suffix
        self.display = display
        self.margin_before = margin_before
        self.margin_after = margin_after
        self.padding = padding
        self.whitespace = whitespace
        self.limit_whitespace_affixes = limit_whitespace_affixes

    def get_refined_html_element(self, new):
        '''
        Args:
            new: The new HtmlElement to be applied to the current context.

        Returns:
            The refined element with the context applied.
        '''
        display = Display.none if self.display == Display.none else new.display
        whitespace = new.whitespace or self.whitespace

        # do not display whitespace only affixes in Whitespace.pre areas
        # if `limit_whitespace_affixes` is set.
        prefix = new.prefix
        suffix = new.suffix
        if new.limit_whitespace_affixes and whitespace == WhiteSpace.pre:
            if prefix.isspace():
                prefix = ''
            if suffix.isspace():
                suffix = ''
        return HtmlElement(new.tag, prefix, suffix, display,
                           new.margin_before, new.margin_after, new.padding,
                           whitespace)

    def clone(self):
        '''
        Returns:
           a clone of the current HtmlElement
        '''
        return HtmlElement(self.tag, self.prefix, self.suffix, self.display,
                           self.margin_before, self.margin_after, self.padding,
                           self.whitespace)

    def __str__(self):
        return (
            '<{self.tag} prefix={self.prefix}, suffix={self.suffix}, '
            'display={self.display}, margin_before={self.margin_before}, '
            'margin_after={self.margin_after}, padding={self.padding}, '
            'whitespace={self.whitespace}>'
        ).format(self=self)


class CssParse():
    '''
    Parses CSS specifications and translates them into the corresponding
    HtmlElements.

    The attribute `display: none`, for instance, is translated to
    `HtmlElement.display=Display.none`.
    '''
    # used to separate value and unit from each other
    RE_UNIT = re_compile(r'([\-0-9\.]+)(\w+)')

    @staticmethod
    def get_style_attribute(style_attribute, html_element):
        '''
        Args:
          style_directive: The attribute value of the given style sheet.
                           Example: display: none
          html_element: The HtmlElement to which the given style is applied.

        Returns:
          An HtmlElement that merges the given element with the style
          attributes specified.
        '''
        custome_html_element = html_element.clone()
        for style_directive in style_attribute.lower().split(';'):
            if ':' not in style_directive:
                continue
            key, value = (s.strip() for s in style_directive.split(':', 1))

            try:
                apply_style = getattr(CssParse, "attr_" +
                                      key.replace('-webkit-', '')
                                      .replace("-", "_"))
                apply_style(value, custome_html_element)
            except AttributeError:
                pass

        return custome_html_element

    @staticmethod
    def _get_em(length):
        '''
        Args:
          length (str): the length (e.g. 2em, 2px, etc.) as specified in the
                        CSS.

        Returns:
            int -- the length in em's.
        '''
        _m = CssParse.RE_UNIT.search(length)
        value = float(_m.group(1))
        unit = _m.group(2)

        if unit not in ('em', 'qem', 'rem'):
            return int(round(value/8))
        return int(round(value))

    # ------------------------------------------------------------------------
    # css styles
    # ------------------------------------------------------------------------

    @staticmethod
    def attr_display(value, html_element):
        '''
        Set the display value.
        '''
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
        '''
        Set the white-space value.
        '''
        if value in ('normal', 'nowrap'):
            html_element.whitespace = WhiteSpace.normal
        elif value in ('pre', 'pre-line', 'pre-wrap'):
            html_element.whitespace = WhiteSpace.pre

    @staticmethod
    def attr_margin_top(value, html_element):
        '''
        Sets the top margin for the given HTML element.
        '''
        html_element.margin_before = CssParse._get_em(value)

    @staticmethod
    def attr_margin_bottom(value, html_element):
        '''
        Sets the bottom margin for the given HTML element.
        '''
        html_element.margin_after = CssParse._get_em(value)

    @staticmethod
    def attr_padding_left(value, html_element):
        '''
        Sets the left padding for the given HTML element.
        '''
        html_element.padding = CssParse._get_em(value)

    # register aliases
    attr_margin_before = attr_margin_top
    attr_margin_after = attr_margin_bottom
    attr_padding_start = attr_padding_left

#!/usr/bin/env python
# coding: utf-8
"""
This module implements basic CSS support for inscriptis.

- The :class:`HtmlElement` class encapsulates all CSS properties of a single
  HTML element.
- :class:`CssParse` parses CSS specifications and translates them into the
  corresponding HtmlElements used by Inscriptis for rendering HTML pages.
"""
from re import compile as re_compile
from inscriptis.html_properties import (Display, WhiteSpace,
                                        HorizontalAlignment, VerticalAlignment)


class HtmlElement:
    """
    The HtmlElement class stores the following CSS properties of HTML
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
      elements with `normal` whitespace handling.
    """

    __slots__ = ('canvas', 'tag', 'prefix', 'suffix', 'display',
                 'margin_before', 'margin_after', 'padding', 'list_bullet',
                 'whitespace', 'limit_whitespace_affixes', 'align', 'valign',
                 'is_empty')

    def __init__(self, tag='default', prefix='', suffix='', display=Display.inline,
                 margin_before=0, margin_after=0, padding=0, list_bullet='',
                 whitespace=None, limit_whitespace_affixes=False,
                 align=HorizontalAlignment.left,
                 valign=VerticalAlignment.middle):
        self.canvas = None
        self.tag = tag
        self.prefix = prefix
        self.suffix = suffix
        self.display = display
        self.margin_before = margin_before
        self.margin_after = margin_after
        self.padding = padding
        self.list_bullet = list_bullet
        self.whitespace = whitespace
        self.limit_whitespace_affixes = limit_whitespace_affixes
        self.align = align
        self.valign = valign
        self.is_empty = True       # whether this is an empty element

    def write(self, text):
        """
        Writes the given HTML text.
        """
        if not (text and not text.isspace()):
            return

        self.is_empty = False
        HtmlElement.WRITER[self.display](self, text)

    def write_tail(self, text):
        if not text:
            return

        if self.display == Display.block and text:
            self.canvas.write_block(self, '\n' * self.margin_after + ' ' * self.padding)
        self.write_inline_text(text)

    def set_canvas(self, canvas):
        self.canvas = canvas
        return self

    def write_inline_text(self, text):
        """
        Writes floating HTML text. All whitespaces are collapsed.
        Args:
            text: the text to write
        """
        self.canvas.write_inline(self,
                                 ''.join((self.prefix, text, self.suffix)))

    def write_block_text(self, text):
        """
        Writes floating HTML text. All whitespaces are collapsed.
        Args:
            text: the text to write
        """
        self.canvas.write_block(self, ''.join(
            (
                '\n' * self.margin_before,
                ' ' * (self.padding - len(self.list_bullet)),
                self.list_bullet,
                self.prefix,
                text.lstrip(),
                self.suffix
            )
        ))

    def write_display_none(self, text):
        return

    def write_verbatim_text(self, text):
        """
        Writes the given text verbatim to the canvas.
        Args:
            text: the text to write
        """
        if not text:
            return
        base_padding = ' ' * self.padding
        self.canvas.write_block(self, text.replace('\n', '\n' + base_padding))

    def get_refined_html_element(self, new):
        """
        Args:
            new: The new HtmlElement to be applied to the current context.

        Returns:
            The refined element with the context applied.
        """
        new.canvas = self.canvas
        if self.is_empty:
            new.list_bullet = self.list_bullet

        # inherit `display:none` attributes and ignore further refinements
        if self.display == Display.none:
            new.display = Display.none
            return new

        # no whitespace set => inherit
        new.whitespace = new.whitespace or self.whitespace

        # do not display whitespace only affixes in Whitespace.pre areas
        # if `limit_whitespace_affixes` is set.
        if (new.limit_whitespace_affixes
                and self.whitespace == WhiteSpace.pre):
            if new.prefix.isspace():
                new.prefix = ''
            if new.suffix.isspace():
                new.suffix = ''

        # total padding = current padding + the padding the refined element
        # introduces
        new.padding += self.padding

        # `Display.block` requires adjusting the `margin_before' and
        # `margin_after` attributes
        if new.display == Display.block:
            if self.tag == 'body':
                new.margin_before = 0
            else:
                new.margin_before = max(new.margin_before,
                                        self.margin_before)
            new.margin_after = max(new.margin_after,
                                   self.margin_after)
        return new

    WRITER = {
        Display.block: write_block_text,
        Display.inline: write_inline_text,
        Display.none: write_display_none
    }

    def __str__(self):
        return (
            '<{self.tag} prefix={self.prefix}, suffix={self.suffix}, '
            'display={self.display}, margin_before={self.margin_before}, '
            'margin_after={self.margin_after}, padding={self.padding}, '
            'list_bullet={self.list_bullet}, '
            'whitespace={self.whitespace}, align={self.align}, '
            'valign={self.valign}>'
        ).format(self=self)


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
                apply_style = getattr(CssParse, "attr_"
                                      + key.replace('-webkit-', '')
                                      .replace("-", "_"))
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
        Apply the given left padding.
        """
        html_element.padding = CssParse._get_em(value)

    @staticmethod
    def attr_horizontal_align(value, html_element):
        """
        Apply the provided horizontal alignment.
        """
        try:
            html_element.align = HorizontalAlignment[value]
        except KeyError:
            pass

    @staticmethod
    def attr_vertical_align(value, html_element):
        """
        Apply the given vertical alignment.
        """
        try:
            html_element.valign = VerticalAlignment[value]
        except KeyError:
            pass

    # register aliases
    attr_margin_before = attr_margin_top
    attr_margin_after = attr_margin_bottom
    attr_padding_start = attr_padding_left

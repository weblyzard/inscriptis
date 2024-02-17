"""Implement basic CSS support for inscriptis.

- The :class:`~inscriptis.model.html_element.HtmlElement` class
  encapsulates all CSS properties of a single HTML element.
- :class:`CssParse` parses CSS specifications and translates them into the
  corresponding HtmlElements used by Inscriptis for rendering HTML pages.
"""
from contextlib import suppress
from re import compile as re_compile

from inscriptis.html_properties import (
    Display,
    WhiteSpace,
    HorizontalAlignment,
    VerticalAlignment,
)
from inscriptis.model.html_element import HtmlElement


class CssParse:
    """Parse CSS specifications and applies them to HtmlElements.

    The attribute `display: none`, for instance, is translated to
    :attr:`HtmlElement.display=Display.none`.
    """

    # used to separate value and unit from each other
    RE_UNIT = re_compile(r"(-?[0-9.]+)(\w+)")

    @staticmethod
    def attr_style(style_attribute: str, html_element: HtmlElement):
        """Apply the provided style attributes to the given HtmlElement.

        Args:
          style_attribute: The attribute value of the given style sheet.
                           Example: display: none
          html_element: The HtmlElement to which the given style is applied.
        """
        for style_directive in style_attribute.lower().split(";"):
            if ":" not in style_directive:
                continue
            key, value = (s.strip() for s in style_directive.split(":", 1))

            try:
                apply_style = getattr(
                    CssParse, "attr_" + key.replace("-webkit-", "").replace("-", "_")
                )
                apply_style(value, html_element)
            except AttributeError:
                pass

    @staticmethod
    def _get_em(length: str) -> int:
        """Convert length specifications into em.

        This function takes a length specification (e.g., 2em, 2px, etc.) and
        transforms it into em.

        Args:
          length: the length specification.

        Returns:
            the length in em.
        """
        _m = CssParse.RE_UNIT.search(length)
        value = float(_m.group(1))
        unit = _m.group(2)

        if unit not in ("em", "qem", "rem"):
            return int(round(value / 8))
        return int(round(value))

    # ------------------------------------------------------------------------
    # css styles
    # ------------------------------------------------------------------------

    @staticmethod
    def attr_display(value: str, html_element: HtmlElement):
        """Apply the given display value."""
        if html_element.display == Display.none:
            return

        if value == "block":
            html_element.display = Display.block
        elif value == "none":
            html_element.display = Display.none
        else:
            html_element.display = Display.inline

    @staticmethod
    def attr_white_space(value: str, html_element: HtmlElement):
        """Apply the given white-space value."""
        if value in ("normal", "nowrap"):
            html_element.whitespace = WhiteSpace.normal
        elif value in ("pre", "pre-line", "pre-wrap"):
            html_element.whitespace = WhiteSpace.pre

    @staticmethod
    def attr_margin_top(value: str, html_element: HtmlElement):
        """Apply the given top margin."""
        with suppress(ValueError):
            html_element.margin_before = CssParse._get_em(value)

    @staticmethod
    def attr_margin_bottom(value: str, html_element: HtmlElement):
        """Apply the provided bottom margin."""
        with suppress(ValueError):
            html_element.margin_after = CssParse._get_em(value)

    @staticmethod
    def attr_padding_left(value: str, html_element: HtmlElement):
        """Apply the given left padding_inline."""
        with suppress(ValueError):
            html_element.padding_inline = CssParse._get_em(value)

    @staticmethod
    def attr_horizontal_align(value: str, html_element: HtmlElement):
        """Apply the provided horizontal alignment."""
        with suppress(KeyError):
            html_element.align = HorizontalAlignment[value]

    @staticmethod
    def attr_vertical_align(value: str, html_element: HtmlElement):
        """Apply the given vertical alignment."""
        with suppress(KeyError):
            html_element.valign = VerticalAlignment[value]

    # register aliases
    attr_margin_before = attr_margin_top
    attr_margin_after = attr_margin_bottom
    attr_padding_start = attr_padding_left

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
    HorizontalAlignment,
    VerticalAlignment,
    WhiteSpace,
)
from inscriptis.model.html_element import HtmlElement

# upper limit for length specifications to prevent
# unbound memory allocation by malformed HTML.
MAX_EM_LEN = 100000
MAX_CSS_LEN = 150

# The CSS length units that are supported by Inscriptis
# and their approximate conversion factors.
CSS_UNIT_TO_EM = {
    "px": 1 / 8,
    "pt": 96 / 72 / 8,
    "pc": 16 / 8,
    "in": 96 / 8,
    "cm": 96 / 2.54 / 8,
    "mm": 96 / 25.4 / 8,
    "q": 96 / 101.6 / 8,
    "em": 1,
    "rem": 1,
    "ex": 0.5,
}


class CssParse:
    """Parse CSS specifications and applies them to HtmlElements.

    The attribute `display: none`, for instance, is translated to
    :attr:`HtmlElement.display=Display.none`.
    """

    # used to separate value and unit from each other
    RE_UNIT = re_compile(
        r"[ \t]*"
        r"(-?(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+))"
        r"(" + "|".join(CSS_UNIT_TO_EM.keys()) + r")"
        r"[ \t]*"
    )

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
                apply_style = getattr(CssParse, "attr_" + key.replace("-webkit-", "").replace("-", "_"))
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
        if len(length) > MAX_CSS_LEN:
            return 0
        if _m := CssParse.RE_UNIT.fullmatch(length.lower()):
            value = float(_m.group(1))
            unit = _m.group(2)
            value *= CSS_UNIT_TO_EM[unit]
            return min(round(value), MAX_EM_LEN)
        return 0

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
        html_element.margin_before = CssParse._get_em(value)

    @staticmethod
    def attr_margin_bottom(value: str, html_element: HtmlElement):
        """Apply the provided bottom margin."""
        html_element.margin_after = CssParse._get_em(value)

    @staticmethod
    def attr_padding_left(value: str, html_element: HtmlElement):
        """Apply the given left padding_inline."""
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

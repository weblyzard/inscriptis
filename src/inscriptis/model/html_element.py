"""Data structures for handling HTML Elements."""
from typing import Tuple

from inscriptis.html_properties import (
    Display,
    HorizontalAlignment,
    VerticalAlignment,
    WhiteSpace,
)


class HtmlElement:
    """The HtmlElement class stores properties and metadata of HTML elements.

    Attributes:
    - canvas: the canvas to which the HtmlElement writes its content.
    - tag: tag name of the given HtmlElement.
    - prefix: specifies a prefix that to insert before the tag's content.
    - suffix: a suffix to append after the tag's content.
    - display: :class:`~inscriptis.html_properties.Display` strategy used for
      the content.
    - margin_before: vertical margin before the tag's content.
    - margin_after: vertical margin after the tag's content.
    - padding_inline: horizontal padding_inline before the tag's content.
    - whitespace: the :class:`~inscriptis.html_properties.Whitespace` handling
      strategy.
    - limit_whitespace_affixes: limit printing of whitespace affixes to
      elements with `normal` whitespace handling.
    - align: the element's horizontal alignment.
    - valign: the element's vertical alignment.
    - previous_margin_after: the margin after of the previous HtmlElement.
    - annotation: annotations associated with the HtmlElement.
    """

    __slots__ = (
        "canvas",
        "tag",
        "prefix",
        "suffix",
        "display",
        "margin_before",
        "margin_after",
        "padding_inline",
        "list_bullet",
        "whitespace",
        "limit_whitespace_affixes",
        "align",
        "valign",
        "previous_margin_after",
        "annotation",
    )

    def __init__(
        self,
        tag: str = "default",
        prefix: str = "",
        suffix: str = "",
        display: Display = Display.inline,
        margin_before: int = 0,
        margin_after: int = 0,
        padding_inline: int = 0,
        list_bullet: str = "",
        whitespace: WhiteSpace = None,
        limit_whitespace_affixes: bool = False,
        align: HorizontalAlignment = HorizontalAlignment.left,
        valign: VerticalAlignment = VerticalAlignment.middle,
        annotation: Tuple[str] = (),
    ):
        self.canvas = None
        self.tag = tag
        self.prefix = prefix
        self.suffix = suffix
        self.display = display
        self.margin_before = margin_before
        self.margin_after = margin_after
        self.padding_inline = padding_inline
        self.list_bullet = list_bullet
        self.whitespace = whitespace
        self.limit_whitespace_affixes = limit_whitespace_affixes
        self.align = align
        self.valign = valign
        self.previous_margin_after = 0
        self.annotation = annotation

    def __copy__(self) -> "HtmlElement":
        """Performance-optimized copy implementation."""
        copy = self.__class__.__new__(self.__class__)
        for attr in self.__slots__:
            setattr(copy, attr, getattr(self, attr))
        return copy

    def write(self, text: str):
        """Write the given HTML text to the element's canvas."""
        if not text or self.display == Display.none:
            return
        self.canvas.write(self, "".join((self.prefix, text, self.suffix)))

    def set_canvas(self, canvas) -> "HtmlElement":
        self.canvas = canvas
        return self

    def set_tag(self, tag: str) -> "HtmlElement":
        self.tag = tag
        return self

    def write_verbatim_text(self, text: str):
        """Write the given text with `Whitespace.pre` to the canvas.

        Args:
            text: the text to write
        """
        if not text:
            return

        if self.display == Display.block:
            self.canvas.open_block(self)

        self.canvas.write(self, text, whitespace=WhiteSpace.pre)

        if self.display == Display.block:
            self.canvas.close_block(self)

    def get_refined_html_element(self, new: "HtmlElement") -> "HtmlElement":
        """Compute the new HTML element based on the previous one.

        Adaptations:
            margin_top: additional margin required when considering
                        margin_bottom of the previous element

        Args:
            new: The new HtmlElement to be applied to the current context.

        Returns:
            The refined element with the context applied.
        """
        new.canvas = self.canvas

        # inherit `display:none` attributes and ignore further refinements
        if self.display == Display.none:
            new.display = Display.none
            return new

        # no whitespace set => inherit
        new.whitespace = new.whitespace or self.whitespace

        # do not display whitespace only affixes in Whitespace.pre areas
        # if `limit_whitespace_affixes` is set.
        if new.limit_whitespace_affixes and self.whitespace == WhiteSpace.pre:
            if new.prefix.isspace():
                new.prefix = ""
            if new.suffix.isspace():
                new.suffix = ""

        if new.display == Display.block and self.display == Display.block:
            new.previous_margin_after = self.margin_after

        return new

    def __str__(self) -> str:
        return (
            f"<{self.tag} prefix={self.prefix}, suffix={self.suffix}, "
            f"display={self.display}, margin_before={self.margin_before}, "
            f"margin_after={self.margin_after}, "
            f"padding_inline={self.padding_inline}, "
            f"list_bullet={self.list_bullet}, "
            f"whitespace={self.whitespace}, align={self.align}, "
            f"valign={self.valign}, annotation={self.annotation}>"
        )

    __repr__ = __str__


"""
An empty default HTML element.
"""
DEFAULT_HTML_ELEMENT = HtmlElement()

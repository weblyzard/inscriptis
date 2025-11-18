"""Represents the state of an HTML document.

The provided `HtmlDocumentState` class contains and exposes all fields required for
representing the current state of the HTML to text conversion.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from inscriptis.model.canvas import Canvas
from inscriptis.model.html_element import DEFAULT_HTML_ELEMENT

if TYPE_CHECKING:
    from inscriptis import ParserConfig


class HtmlDocumentState:
    """Represents the state of the parsed html document."""

    def __init__(self, config: ParserConfig):
        # instance variables
        self.canvas = Canvas()
        self.config = config
        self.css = config.css
        self.apply_attributes = config.attribute_handler.apply_attributes

        self.tags = [self.css["body"].set_canvas(self.canvas)]
        self.current_table = []
        self.li_counter = []
        self.last_caption = None

        # used if display_links is enabled
        self.link_target = ""

    def apply_starttag_layout(self, tag, attrs):
        """Compute the layout of the tag.

        Compute the style of the current :class:`HtmlElement`, based on

        1. the used :attr:`css`,
        2. apply attributes and css with :meth:`~Attribute.apply_attributes`
        3. add the `HtmlElement` to the list of open tags.

        Args:
          tag: the HTML start tag to process.
          attrs: a dictionary of HTML attributes and their respective values.

        """
        # use the css to handle tags known to it :)
        cur = self.tags[-1].get_refined_html_element(
            self.apply_attributes(
                attrs,
                html_element=self.css.get(tag, DEFAULT_HTML_ELEMENT).__copy__().set_tag(tag),
            ),
        )
        self.tags.append(cur)

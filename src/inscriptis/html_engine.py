#!/usr/bin/env python
"""The HTML Engine is responsible for converting HTML to text."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lxml.etree import Comment

from inscriptis.model.config import ParserConfig
from inscriptis.model.html_document_state import HtmlDocumentState
from inscriptis.model.tag.a_tag import a_end_handler, a_start_handler
from inscriptis.model.tag.br_tag import br_start_handler
from inscriptis.model.tag.img_tag import img_start_handler
from inscriptis.model.tag.list_tag import (
    li_start_handler,
    ol_end_handler,
    ol_start_handler,
    ul_end_handler,
    ul_start_handler,
)
from inscriptis.model.tag.table_tag import (
    table_end_handler,
    table_start_handler,
    td_end_handler,
    td_start_handler,
    tr_start_handler,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    import lxml.html

    from inscriptis.annotation import Annotation
    from inscriptis.model.canvas import Canvas


class Inscriptis:
    """Translate an lxml HTML tree to the corresponding text representation.

    Args:
      html_tree: the lxml HTML tree to convert.
      config: an optional ParserConfig configuration object.

    Example::

      from lxml.html import fromstring
      from inscriptis.html_engine import Inscriptis

      html_content = "<html><body><h1>Test</h1></body></html>"

      # create an HTML tree from the HTML content.
      html_tree = fromstring(html_content)

      # transform the HTML tree to text.
      parser = Inscriptis(html_tree)
      text = parser.get_text()

    """

    def __init__(self, html_tree: lxml.html.HtmlElement, config: ParserConfig = None) -> None:
        # use the default configuration, if no config object is provided
        config = config or ParserConfig()

        # setup start and end tag call tables
        self.start_tag_handler_dict: dict[str, Callable[[HtmlDocumentState, dict], None]] = {
            "table": table_start_handler,
            "tr": tr_start_handler,
            "td": td_start_handler,
            "th": td_start_handler,
            "ul": ul_start_handler,
            "ol": ol_start_handler,
            "li": li_start_handler,
            "br": br_start_handler,
            "a": a_start_handler if config.parse_a() else None,
            "img": img_start_handler if config.display_images else None,
        }
        self.end_tag_handler_dict: dict[str, Callable[[HtmlDocumentState], None]] = {
            "table": table_end_handler,
            "ul": ul_end_handler,
            "ol": ol_end_handler,
            "td": td_end_handler,
            "th": td_end_handler,
            "a": a_end_handler if config.parse_a() else None,
        }

        if config.custom_html_tag_handler_mapping:
            self.start_tag_handler_dict.update(config.custom_html_tag_handler_mapping.start_tag_mapping)
            self.end_tag_handler_dict.update(config.custom_html_tag_handler_mapping.end_tag_mapping)

        # parse the HTML tree
        self.canvas = self._parse_html_tree(HtmlDocumentState(config), html_tree)

    def _parse_html_tree(self, state: HtmlDocumentState, tree) -> Canvas:
        """Parse the HTML tree.

        Args:
            state: the current HTML document state.
            tree: the HTML tree to parse.

        """
        if isinstance(tree.tag, str):
            state.apply_starttag_layout(tree.tag, tree.attrib)

            if handler := self.start_tag_handler_dict.get(tree.tag):
                handler(state, tree.attrib)
            cur = state.tags[-1]
            cur.canvas.open_tag(cur)

            state.tags[-1].write(tree.text)

            for node in tree:
                self._parse_html_tree(state, node)

            # handle the endtag
            if handler := self.end_tag_handler_dict.get(tree.tag):
                handler(state)
            prev = state.tags.pop()
            prev.canvas.close_tag(prev)

            # write the tail text to the element's container
            state.tags[-1].write(tree.tail)

        elif tree.tag is Comment and tree.tail:
            state.tags[-1].canvas.write(state.tags[-1], tree.tail)

        return state.canvas

    def get_text(self) -> str:
        """Return the text extracted from the HTML page."""
        return self.canvas.get_text()

    def get_annotations(self) -> list[Annotation]:
        """Return the annotations extracted from the HTML page."""
        return self.canvas.annotations

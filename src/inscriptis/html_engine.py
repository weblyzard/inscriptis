#!/usr/bin/env python
# coding:utf-8
"""The HTML Engine is responsible for converting HTML to text."""
from typing import List

import lxml.html
from lxml.etree import Comment

from inscriptis.annotation import Annotation
from inscriptis.model.canvas import Canvas
from inscriptis.model.config import ParserConfig
from inscriptis.model.html_document_state import HtmlDocumentState
from inscriptis.model.html_element import DEFAULT_HTML_ELEMENT
from inscriptis.model.tag.a_tag import a_start_handler, a_end_handler
from inscriptis.model.tag.br_tag import br_start_handler
from inscriptis.model.tag.img_tag import img_start_handler
from inscriptis.model.tag.list_tag import (
    ul_start_handler,
    ol_start_handler,
    li_start_handler,
    ul_end_handler,
    ol_end_handler,
)
from inscriptis.model.tag.table_tag import (
    table_start_handler,
    tr_start_handler,
    td_start_handler,
    table_end_handler,
    td_end_handler,
)


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

    def __init__(self, html_tree: lxml.html.HtmlElement, config: ParserConfig = None):
        # use the default configuration, if no config object is provided
        self.config = config or ParserConfig()

        # setup start and end tag call tables
        self.start_tag_handler_dict = {
            "table": table_start_handler,
            "tr": tr_start_handler,
            "td": td_start_handler,
            "th": td_start_handler,
            "ul": ul_start_handler,
            "ol": ol_start_handler,
            "li": li_start_handler,
            "br": br_start_handler,
            "a": a_start_handler if self.config.parse_a() else None,
            "img": img_start_handler if self.config.display_images else None,
        }
        self.end_tag_handler_dict = {
            "table": table_end_handler,
            "ul": ul_end_handler,
            "ol": ol_end_handler,
            "td": td_end_handler,
            "th": td_end_handler,
            "a": a_end_handler if self.config.parse_a() else None,
        }

        # parse the HTML tree
        state = HtmlDocumentState(config)
        self.canvas = self._parse_html_tree(state, html_tree)

    def _parse_html_tree(self, state: HtmlDocumentState, tree) -> Canvas:
        """Parse the HTML tree.

        Args:
            tree: the HTML tree to parse.
        """
        if isinstance(tree.tag, str):
            self.handle_starttag(state, tree.tag, tree.attrib)
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

    def get_annotations(self) -> List[Annotation]:
        """Return the annotations extracted from the HTML page."""
        return self.canvas.annotations

    def handle_starttag(self, state, tag, attrs, handler):
        """Handle HTML start tags.

        Compute the style of the current :class:`HtmlElement`, based on

        1. the used :attr:`css`,
        2. apply attributes and css with :meth:`~Attribute.apply_attributes`
        3. add the `HtmlElement` to the list of open tags.

        Lookup and apply and tag-specific start tag handler in
        :attr:`start_tag_handler_dict`.

        Args:
          tag: the HTML start tag to process.
          attrs: a dictionary of HTML attributes and their respective values.
        """
        # use the css to handle tags known to it :)
        cur = state.tags[-1].get_refined_html_element(
            state.apply_attributes(
                attrs,
                html_element=state.css.get(tag, DEFAULT_HTML_ELEMENT)
                .__copy__()
                .set_tag(tag),
            )
        )
        state.tags.append(cur)

        if handler:
            handler(attrs)

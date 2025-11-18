#!/usr/bin/env python3

"""Custom HTML tag handling example.

Add a custom HTML handler for the bold <b> tag which encloses
bold text with "**".

Example:
    "Welcome to <b>Chur</b>" is rendered as "Welcome to **Chur**".

"""

from lxml.html import fromstring

from inscriptis import ParserConfig
from inscriptis.html_engine import Inscriptis
from inscriptis.model.html_document_state import HtmlDocumentState
from inscriptis.model.tag import CustomHtmlTagHandlerMapping


def my_handle_start_b(state: HtmlDocumentState, _: dict) -> None:
    """Handle the opening <b> tag."""
    state.tags[-1].write("**")


def my_handle_end_b(state: HtmlDocumentState) -> None:
    """Handle the closing </b> tag."""
    state.tags[-1].write("**")


MY_MAPPING = CustomHtmlTagHandlerMapping(
    start_tag_mapping={"b": my_handle_start_b},
    end_tag_mapping={"b": my_handle_end_b},
)


HTML = "Welcome to <b>Chur</b>"

html_tree = fromstring(HTML)
inscriptis = Inscriptis(html_tree, ParserConfig(custom_html_tag_handler_mapping=MY_MAPPING))
print(inscriptis.get_text())

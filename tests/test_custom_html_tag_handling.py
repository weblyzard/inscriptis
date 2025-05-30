"""Test the custom HTML tag handling."""

from lxml.html import fromstring

from inscriptis import Inscriptis
from inscriptis.model.config import ParserConfig
from inscriptis.model.html_document_state import HtmlDocumentState
from inscriptis.model.tag import CustomHtmlTagHandlerMapping


def test_custom_html_handler():
    def my_handle_start_b(state: HtmlDocumentState, _):
        """Handle the opening <b> tag."""
        state.tags[-1].write("**")

    def my_handle_end_b(state: HtmlDocumentState):
        """Handle the closing </b> tag."""
        state.tags[-1].write("**")

    custom_mapping = CustomHtmlTagHandlerMapping(
        start_tag_mapping={"b": my_handle_start_b},
        end_tag_mapping={"b": my_handle_end_b},
    )

    html_tree = fromstring("Welcome to <b>Chur</b>")
    inscriptis = Inscriptis(html_tree, ParserConfig(custom_html_tag_handler_mapping=custom_mapping))

    # custom HTML Handler
    assert inscriptis.get_text().strip() == "Welcome to **Chur**"
    # standard HTML handler
    assert Inscriptis(html_tree).get_text().strip() == "Welcome to Chur"

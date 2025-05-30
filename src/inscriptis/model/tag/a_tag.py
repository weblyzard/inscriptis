"""Handle the <a> tag."""

from inscriptis.model.html_document_state import HtmlDocumentState


def a_start_handler(state: HtmlDocumentState, attrs: dict) -> None:
    """Handle the <a> tag."""
    state.link_target = ""
    if state.config.display_links:
        state.link_target = attrs.get("href", "")
    if state.config.display_anchors:
        state.link_target = state.link_target or attrs.get("name", "")

    if state.link_target:
        state.tags[-1].write("[")


def a_end_handler(state: HtmlDocumentState) -> None:
    """Handle the </a> tag."""
    if state.link_target:
        state.tags[-1].write(f"]({state.link_target})")

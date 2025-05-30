"""Handle the <br> tag."""

from inscriptis.model.html_document_state import HtmlDocumentState


def br_start_handler(state: HtmlDocumentState, _: dict) -> None:
    """Handle the <br> tag."""
    state.tags[-1].canvas.write_newline()

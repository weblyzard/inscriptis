"""Handle the <br> tag."""
from typing import Dict

from inscriptis.model.html_document_state import HtmlDocumentState


def br_start_handler(state: HtmlDocumentState, _: Dict) -> None:
    """Handle the <br> tag."""
    state.tags[-1].canvas.write_newline()

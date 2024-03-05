"""Handle the <img> tag."""
from typing import Dict

from inscriptis.model.html_document_state import HtmlDocumentState


def img_start_handler(state: HtmlDocumentState, attrs: Dict) -> None:
    """Handle the <img> tag."""
    image_text = attrs.get("alt", "") or attrs.get("title", "")
    if image_text and not (
        state.config.deduplicate_captions and image_text == state.last_caption
    ):
        state.tags[-1].write(f"[{image_text}]")
        state.last_caption = image_text

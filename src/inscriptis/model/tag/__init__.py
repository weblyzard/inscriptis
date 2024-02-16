"""HTML Tag handlers and classes for designing custom HTML tag handlers."""
from __future__ import annotations
from typing import Dict, Callable, NamedTuple

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from inscriptis.model.html_document_state import HtmlDocumentState


class CustomHtmlTagHandlerMapping(NamedTuple):
    """Provide a custom HTML Tag handler mapping."""

    start_tag_handler_mapping: Dict[str, Callable[[HtmlDocumentState, Dict], None]]
    end_tag_handler_mapping: Dict[str, Callable[[HtmlDocumentState], None]]

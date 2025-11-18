"""HTML Tag handlers and classes for designing custom HTML tag handlers."""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from collections.abc import Callable

    from inscriptis.model.html_document_state import HtmlDocumentState


class CustomHtmlTagHandlerMapping(NamedTuple):
    """Refine the standard HTML Tag handling with the provided mapping.

    Attributes:
        start_tag_mapping: a dictionary of custom start tag handlers.
        end_tag_mapping: a dictionary of custom end tag handlers.

    """

    start_tag_mapping: dict[str, Callable[[HtmlDocumentState, dict], None]]
    end_tag_mapping: dict[str, Callable[[HtmlDocumentState], None]]

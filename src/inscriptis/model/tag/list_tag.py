"""Handle the <li>, <ol>, <ul> tags."""

from inscriptis.model.html_document_state import HtmlDocumentState

UL_COUNTER = ("* ", "+ ", "o ", "- ")
UL_COUNTER_LEN = len(UL_COUNTER)


def get_bullet(state: HtmlDocumentState) -> str:
    """Return the bullet that correspond to the given index."""
    return UL_COUNTER[len(state.li_counter) % UL_COUNTER_LEN]


def li_start_handler(state: HtmlDocumentState, tag: dict) -> None:
    """Handle the <li> tag."""
    bullet = state.li_counter[-1] if state.li_counter else "* "
    # Value can only used for numerical bullets.
    if "value" in tag and tag["value"].isdigit() and isinstance(bullet, int):
        bullet = int(tag["value"])
        state.li_counter[-1] = bullet

    if isinstance(bullet, int):
        state.li_counter[-1] += 1
        state.tags[-1].list_bullet = f"{bullet}. "
    else:
        state.tags[-1].list_bullet = bullet

    state.tags[-1].write("")


def ul_start_handler(state: HtmlDocumentState, _: dict) -> None:
    """Handle the <ul> tag."""
    state.li_counter.append(get_bullet(state))


def ul_end_handler(state: HtmlDocumentState) -> None:
    """Handle the </ul> tag."""
    state.li_counter.pop()


def ol_start_handler(state: HtmlDocumentState, _: dict) -> None:
    """Handle the <ol> tag."""
    state.li_counter.append(1)


def ol_end_handler(state: HtmlDocumentState) -> None:
    """Handle the </ol> tag."""
    state.li_counter.pop()

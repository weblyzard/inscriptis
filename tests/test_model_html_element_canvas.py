#!/usr/bin/env python

"""
Tests the rendering of a single table line.
"""

from inscriptis.html_properties import Display
from inscriptis.model.canvas import Canvas
from inscriptis.model.html_element import HtmlElement


def _get_text(html_element):
    """
    Returns
        the text formatted based on the current HTML element.
    """
    c = Canvas()
    html_element.canvas = c

    HtmlElement().set_canvas(c).write("first")

    c.open_tag(html_element)
    html_element.write("Ehre sei Gott!")
    c.close_tag(html_element)

    HtmlElement().set_canvas(c).write("last")
    c.flush_inline()
    return "\n".join(c.blocks)


def test_formatting():
    # standard line

    h = HtmlElement()
    assert _get_text(h) == "firstEhre sei Gott!last"

    h.display = Display.block
    h.margin_before = 1
    h.margin_after = 2
    print(h)
    print(_get_text(h))
    assert _get_text(h) == "first\n\nEhre sei Gott!\n\n\nlast"

    # list bullet without padding_inline
    h.list_bullet = "* "
    assert _get_text(h) == "first\n\n* Ehre sei Gott!\n\n\nlast"

    # add a padding_inline
    h.padding_inline = 3
    assert _get_text(h) == "first\n\n * Ehre sei Gott!\n\n\nlast"

    # and prefixes + suffixes
    h.prefix = ">>"
    h.suffix = "<<"
    assert _get_text(h) == "first\n\n * >>Ehre sei Gott!<<\n\n\nlast"

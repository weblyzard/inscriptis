#!/usr/bin/env python

"""ensures that two successive <a>text</a> contain
a space between each other, if there is a linebreak
or space between the tags.
"""

from inscriptis import get_text


def test_empty_and_corrupt():
    assert get_text("test").strip() == "test"
    assert get_text("  ") == ""
    assert get_text("") == ""
    # test for the behaviour of older and recent lxml versions.
    assert get_text("<<<").strip() in ("<<<", "<<", "")

#!/usr/bin/env python

"""
Tests the rendering of a single table line.
"""

from inscriptis.model.canvas import Prefix


def test_simple_prefix():
    p = Prefix()

    p.register_prefix(5, "1. ")

    # first use
    assert p.first == "  1. "

    # the prefix has been consumed
    assert p.first == ""

    # prefix used to indent lines separated with newlines
    assert p.rest == "     "


def test_combined_prefix():
    p = Prefix()

    p.register_prefix(5, "1. ")
    p.register_prefix(2, "")

    assert p.first == "    1. "
    assert p.first == ""

    p.remove_last_prefix()
    assert p.first == ""

    p.remove_last_prefix()
    # final consumption - no prefix
    assert p.first == ""

    # ensure that there are no interactions between different runs with
    # bullets
    p.consumed = False
    p.register_prefix(5, "2. ")
    p.register_prefix(2, "- ")

    assert p.first == "     - "
    assert p.first == ""
    assert p.rest == "       "

    p.consumed = False
    p.remove_last_prefix()
    assert p.first == "  2. "
    assert p.rest == "     "

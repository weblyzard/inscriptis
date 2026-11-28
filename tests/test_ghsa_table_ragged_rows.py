#!/usr/bin/env python

"""Ensure that a single table with ragged rows is rendered in linear time.
https://github.com/weblyzard/inscriptis/security/advisories/GHSA-vmxw-xvww-46f9

Verifies the fix for the O(n^2) column-width computation in
``Table._set_column_width`` (one wide row of N cells plus N single-cell rows
previously took time proportional to N squared).
"""

import time

from inscriptis import get_text


def test_ragged_table_is_linear():
    n = 12000
    html = "<table><tr>" + "<td>x</td>" * n + "</tr>" + "<tr><td>y</td></tr>" * n + "</table>"
    start = time.monotonic()
    get_text(html)
    # The quadratic version took several seconds at this size (about 12 s); the
    # linear version is well under a second, so a generous bound catches a regression.
    assert time.monotonic() - start < 5

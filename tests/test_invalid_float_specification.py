#!/usr/bin/env python

"""
Tests handling of invalid length specifications.
(https://github.com/weblyzard/inscriptis/issues/63)
"""

from inscriptis import get_text


def test_invalid_length_specification_handling():
    html = (
        """<p style="margin:0;padding:0;margin: 0cm; margin-bottom: ..0001pt; -ms-word-wrap: break-word;">"""
        """<span style="font-size: 10.0pt; font-family: \'Arial\',sans-serif; color: black;">"""
    )
    print(get_text(html))

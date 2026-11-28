"""Regression tests for output amplification from untrusted HTML.
https://github.com/weblyzard/inscriptis/security/advisories/GHSA-m6p9-2jq4-55qw

The limits below are fixture-specific regression targets, not a general output
size policy. The tests are expected to fail until rendering is bounded.
"""

import pytest

from inscriptis import get_text


@pytest.mark.parametrize("preformatted", [False, True], ids=["paragraphs", "pre"])
def test_nested_padding_output_is_bounded(preformatted):
    line_count = 8
    content = "<pre>" + "\n".join(["x"] * line_count) + "</pre>" if preformatted else "<p>x</p>" * line_count
    html = '<div style="padding-left:100000em">' * 8 + content + "</div>" * 8

    text = get_text(html)

    assert text.count("x") == line_count
    assert len(text) <= 1_000_000


def test_table_column_padding_output_is_bounded():
    width = 1000
    row_count = 1000
    html = "<table><tr><td>" + "a" * width + "</td></tr>" + "<tr><td>b</td></tr>" * row_count + "</table>"

    text = get_text(html)

    assert "a" * width in text
    assert text.count("b") == row_count
    assert len(text) <= 300_000

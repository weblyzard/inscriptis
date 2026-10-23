#!/usr/bin/env python

"""Ensures that HTML fragments are converted without a synthetic wrapper element.

lxml.html.fromstring wraps fragments that consist of multiple root elements or
of top-level text in a synthetic <div> or <span>. The relaxed CSS profile styles
these elements (indentation for div, surrounding spaces for span), which must not
leak into the text representation.
"""

import pytest

from inscriptis import get_annotated_text, get_text
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

STRICT = ParserConfig(css=CSS_PROFILES["strict"])


@pytest.mark.parametrize(
    ("html", "expected"),
    [
        ("<p>a</p>x", "a\n\nx"),
        ("<p>a</p><p>b</p>", "a\n\nb\n"),
        ("<div>a</div><div>b</div>", "  a\n  b"),
        ("<b>a</b>b", "ab"),
        ("<b>bold</b>text", "boldtext"),
        ("<b>un</b>believable", "unbelievable"),
    ],
)
def test_fragment_without_wrapper(html, expected):
    assert get_text(html) == expected


@pytest.mark.parametrize(
    "html",
    [
        "<p>a</p>x",
        "<p>a</p><p>b</p>",
        "<div>a</div><div>b</div>",
        "<b>a</b>b",
        "<b>un</b>believable",
        "<td>a</td><td>b</td>",
        "<p>a</p><!-- comment -->",
    ],
)
@pytest.mark.parametrize("config", [None, STRICT], ids=["relaxed", "strict"])
def test_fragment_equals_body_content(html, config):
    """A fragment yields the same text as the same markup inside an explicit <body>."""
    assert get_text(html, config) == get_text(f"<html><body>{html}</body></html>", config)


def test_fragment_annotations():
    config = ParserConfig(annotation_rules={"b": ["bold"]})
    result = get_annotated_text("<b>un</b>believable", config)
    assert result["text"] == "unbelievable"
    assert result["label"] == [(0, 2, "bold")]


@pytest.mark.parametrize(
    ("html", "expected"),
    [
        ("<p>a</p>", "a\n"),
        ("<div>a</div>", "  a"),
        ("<span>a</span>", "a"),
        ("<li>a</li><li>b</li>", "* a\n* b"),
        ("<html><body><p>a</p>x</body></html>", "a\n\nx"),
        ("<!-- comment -->", ""),
        ("  \n", ""),
        ("", ""),
    ],
)
def test_unchanged_inputs(html, expected):
    """Single elements, full documents and empty input are not affected."""
    assert get_text(html) == expected

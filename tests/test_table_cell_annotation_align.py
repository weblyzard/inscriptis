#!/usr/bin/env python

"""Annotations in single-line table cells must follow horizontal alignment."""

from copy import deepcopy

from inscriptis import get_annotated_text
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

config = ParserConfig(css=deepcopy(CSS_PROFILES["strict"]), annotation_rules={"span": ["s"]})


def test_single_line_center_align_annotation():
    html = "<table><tr><td align='center'><span>x</span></td></tr><tr><td>wwwwww</td></tr></table>"
    result = get_annotated_text(html, config)
    assert result["text"] == "  x   \nwwwwww\n"
    assert result["label"] == [(2, 3, "s")]
    assert result["text"][2:3] == "x"


def test_single_line_right_align_annotation():
    html = "<table><tr><td align='right'><span>x</span></td></tr><tr><td>wwwwww</td></tr></table>"
    result = get_annotated_text(html, config)
    assert result["text"] == "     x\nwwwwww\n"
    assert result["label"] == [(5, 6, "s")]
    assert result["text"][5:6] == "x"


def test_single_line_left_align_annotation():
    html = "<table><tr><td align='left'><span>x</span></td></tr><tr><td>wwwwww</td></tr></table>"
    result = get_annotated_text(html, config)
    assert result["text"] == "x     \nwwwwww\n"
    assert result["label"] == [(0, 1, "s")]
    assert result["text"][0:1] == "x"

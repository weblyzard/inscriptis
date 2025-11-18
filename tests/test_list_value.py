#!/usr/bin/env python

"""Test list value in ordered and unordered lists."""

from inscriptis import get_text
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

config = ParserConfig(css=CSS_PROFILES["strict"])


def test_value():
    html = "<body>Thomas <ol><li> a  <div>Anton</div>Maria</ol></body>"
    assert get_text(html, config) == "Thomas\n 1. a\n    Anton\n    Maria"

    html = """<body>Thomas <ol><li value="2"> a  <div>Anton</div>Maria</ol></body>"""
    assert get_text(html, config) == "Thomas\n 2. a\n    Anton\n    Maria"

    html = """<body>Thomas <ol><li value="2"> a  <ol><li><div>Anton</div></li></ol>Maria</ol></body>"""
    assert get_text(html, config) == "Thomas\n 2. a\n     1. Anton\n    Maria"

    html = """<body>Thomas <ol><li value="2"> a  <ol><li value="10"><div>Anton</div></li></ol>Maria</ol></body>"""
    assert get_text(html, config) == "Thomas\n 2. a\n    10. Anton\n    Maria"


def test_value_without_ol():
    """Behavior if the <ol> tag is missing."""
    html = """<body>Thomas <li value="2">Maria</li><li>Ana</li></body>"""
    assert get_text(html, config) == "Thomas\n* Maria\n* Ana"

    html = """<body>Thomas <li value="2">Maria</li><li>Ana</li></ul></body>"""
    assert get_text(html, config) == "Thomas\n* Maria\n* Ana"

#!/usr/bin/env python

"""
Tests different white-space handling.
"""

from inscriptis import get_text
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

config = ParserConfig(css=CSS_PROFILES["strict"])


def test_white_space():
    html = '<body><span style="white-space: normal"><i>1</i>2\n3</span></body>'
    assert get_text(html, config) == "12 3"

    html = '<body><span style="white-space: nowrap"><i>1</i>2\n3</span></body>'
    assert get_text(html, config) == "12 3"

    html = '<body><span style="white-space: pre"><i>1</i>2\n3</span></body>'
    assert get_text(html, config) == "12\n3"

    html = '<body><span style="white-space: pre-line"><i>1</i>2\n3</span></body>'
    assert get_text(html, config) == "12\n3"

    html = '<body><span style="white-space: pre-wrap"><i>1</i>2\n3</span></body>'
    assert get_text(html, config) == "12\n3"


def test_borderline_cases():
    """
    testing of borderline cases based on the behavior found in Firefox and
    Google Chrome.
    """
    # change of whitespace handling between terms; no whitespace
    # between the terms
    html = '<body>Hallo<span style="white-space: pre">echo</span> versus'
    assert get_text(html, config) == "Halloecho versus"

    # change of whitespace handling between terms; one whitespace
    # between the terms; option 1
    html = '<body>Hallo<span style="white-space: pre"> echo</span> versus'
    assert get_text(html, config) == "Hallo echo versus"

    # change of whitespace handling between terms; one whitespace
    # between the terms; option 2
    html = '<body>Hallo <span style="white-space: pre">echo</span> versus'
    assert get_text(html, config) == "Hallo echo versus"

    # change of whitespace handling between terms; two whitespaces
    # between the terms
    html = '<body>Hallo <span style="white-space: pre"> echo</span> versus'
    assert get_text(html, config) == "Hallo  echo versus"

    # change of whitespace handling between terms; multiple whitespaces
    # between the terms
    html = '<body>Hallo   <span style="white-space: pre"> echo</span> versus'
    assert get_text(html, config) == "Hallo  echo versus"

    # change of whitespace handling between terms; multiple whitespaces
    # between the terms
    html = '<body>Hallo   <span style="white-space: pre">   echo</span> versus'
    assert get_text(html, config) == "Hallo    echo versus"


def test_tail():
    """
    ensure that the tail elements are formated based on the container element.
    """
    html = '<body>Hi<span style="white-space: pre"> 1   3 </span> versus 1   3'
    assert get_text(html, config) == "Hi 1   3  versus 1 3"

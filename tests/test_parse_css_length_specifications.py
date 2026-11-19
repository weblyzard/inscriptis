#!/usr/bin/env python

"""
Tests HtmlElement and the parsing of CSS style definitiosn
"""

import pytest

from inscriptis.model.canvas import Display
from inscriptis.model.css import CSS_UNIT_TO_EM, MAX_CSS_LEN, MAX_EM_LEN, CssParse
from inscriptis.model.html_element import HtmlElement


@pytest.mark.parametrize(
    "value",
    [
        "...",
        "",
        "   ",
        "-",
        ".",
        "-.em",
        "px",
        "-px",
        "garbage",
        "10pxgarbage",
        "10..5px",
        "10 px",
        "10unknownunit",
        "." * 10_000,
        "." * 40_000,
    ],
)
def test_invalid_css_lengths(value):
    assert CssParse._get_em(value) == 0


@pytest.mark.parametrize(
    "value,expected",
    [
        ("0px", 0),
        ("0em", 0),
        ("-0px", 0),
        ("10px", 1),
        ("16px", 2),
        ("10em", 10),
        ("10rem", 10),
        ("10.5px", 1),
        ("-10px", -1),
        ("0.5em", 0),
        (".5em", 0),
        ("-.5em", 0),
        ("1.5em", 2),
        ("-1.5em", -2),
        ("2.px", 0),  # trailing dot without fractional digits
    ],
)
def test_valid_css_lengths(value, expected):
    result = CssParse._get_em(value)
    assert isinstance(result, int)
    assert result == expected


@pytest.mark.parametrize("unit", CSS_UNIT_TO_EM.keys())
def test_all_supported_units(unit):
    sample = f"4{unit}"
    expected = int(min(round(4 * CSS_UNIT_TO_EM[unit]), MAX_EM_LEN))
    assert CssParse._get_em(sample) == expected


def test_css_length_limit():
    # Exceeding MAX_CSS_LEN returns 0
    assert CssParse._get_em("1" * MAX_CSS_LEN + "px") == 0
    # Exactly MAX_CSS_LEN is allowed (e.g., "1" * 148 + "px" == 150 chars)
    exact_len_input = "1" * (MAX_CSS_LEN - 2) + "px"
    assert len(exact_len_input) == MAX_CSS_LEN
    assert isinstance(CssParse._get_em(exact_len_input), int)


def test_max_em_len_clamping():
    assert CssParse._get_em("999999999em") == MAX_EM_LEN


def test_css_length_whitespace():
    assert CssParse._get_em(" 10px ") == CssParse._get_em("10px")
    assert CssParse._get_em("\t2.5em\t") == CssParse._get_em("2.5em")


def test_attr_style_integration():
    el = HtmlElement()
    CssParse.attr_style(
        "margin-top: .5em; MARGIN-BOTTOM: 16px; padding-left: px; display: block",
        el,
    )
    assert el.margin_before == 0
    assert el.margin_after == 2
    assert el.padding_inline == 0
    assert el.display == Display.block

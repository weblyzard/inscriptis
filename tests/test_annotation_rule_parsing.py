#!/usr/bin/env python

"""
Tests the Table formatting with different parameters such as width and
alignment
"""

from copy import deepcopy

from inscriptis.annotation.parser import AnnotationModel
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.attribute import Attribute
from inscriptis.model.html_element import HtmlElement


def test_parse():
    """
    basic rule parsing.
    """
    rules = {"table#border=1": ["table"], "hr": ["horizontal-line"]}
    tags, attrs = AnnotationModel._parse(rules)

    assert tags == {"hr": ["horizontal-line"]}

    apply_annotation = attrs[0]
    assert apply_annotation.match_tag == "table"
    assert apply_annotation.match_value == "1"
    assert apply_annotation.attr == "border"

    e = HtmlElement(tag="table")
    apply_annotation.apply("1", e)
    assert e.annotation == ("table",)


def test_apply_annotation():
    """
    rule application.
    """
    rules = {
        "table#border=1": ["table"],
        "hr": ["horizontal-line"],
        "#color=red": ["red"],
        "#bgcolor": ["bgcolor"],
    }

    css = deepcopy(CSS_PROFILES["strict"])
    annotation_model = AnnotationModel(css, rules)
    assert annotation_model.css["hr"].annotation == ("horizontal-line",)

    attribute_handler = Attribute()
    attribute_handler.merge_attribute_map(annotation_model.css_attr)
    assert "table#border=1" in str(attribute_handler.attribute_mapping["border"])
    assert "{any}#color=red" in str(attribute_handler.attribute_mapping["color"])
    assert "{any}#bgcolor={any}" in str(attribute_handler.attribute_mapping["bgcolor"])


def test_merged_attribute():
    """
    test multiple rules per attribute
    """
    rules = {"#color=white": ["white"], "#color=yellow": ["yellow"]}
    css = deepcopy(CSS_PROFILES["strict"])
    annotation_model = AnnotationModel(css, rules)

    attribute_handler = Attribute()
    attribute_handler.merge_attribute_map(annotation_model.css_attr)

    e = HtmlElement()
    attribute_handler.attribute_mapping["color"]("green", e)
    assert e.annotation == ()
    attribute_handler.attribute_mapping["color"]("yellow", e)
    assert e.annotation == ("yellow",)
    attribute_handler.attribute_mapping["color"]("white", e)
    assert e.annotation == ("yellow", "white")

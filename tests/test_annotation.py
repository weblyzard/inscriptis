#!/usr/bin/env python
# encoding: utf-8

"""
Tests the Table formatting with different parameters such as width and
alignment
"""

from inscriptis.annotation import Annotation, horizontal_shift
from inscriptis.html_properties import HorizontalAlignment


def test_horizontal_shift():
    a = [Annotation(0, 4, "test")]

    # no shift
    assert horizontal_shift(
        a, content_width=5, line_width=10, align=HorizontalAlignment.left, shift=0
    ).pop() == Annotation(0, 4, "test")

    # shift
    assert horizontal_shift(
        a, content_width=5, line_width=10, align=HorizontalAlignment.left, shift=3
    ).pop() == Annotation(3, 7, "test")

    # realignment to the right
    assert horizontal_shift(
        a,
        content_width=len("test"),
        line_width=10,
        align=HorizontalAlignment.right,
        shift=0,
    ).pop() == Annotation(6, 10, "test")
    assert "{:>10}".format("test")[6:10] == "test"

    # shift + realignment to the right
    assert horizontal_shift(
        a,
        content_width=len("test"),
        line_width=10,
        align=HorizontalAlignment.right,
        shift=3,
    ).pop() == Annotation(9, 13, "test")

    # realignment to the center
    assert horizontal_shift(
        a,
        content_width=len("test"),
        line_width=10,
        align=HorizontalAlignment.center,
        shift=0,
    ).pop() == Annotation(3, 7, "test")
    assert "{:^10}".format("test")[3:7] == "test"

    assert horizontal_shift(
        a,
        content_width=len("test"),
        line_width=11,
        align=HorizontalAlignment.center,
        shift=0,
    ).pop() == Annotation(3, 7, "test")
    assert "{:^11}".format("test")[3:7] == "test"

    # realignment + shift
    assert horizontal_shift(
        a,
        content_width=len("test"),
        line_width=11,
        align=HorizontalAlignment.center,
        shift=7,
    ).pop() == Annotation(10, 14, "test")


def test_comparison():
    a = Annotation(24, 62, "tableheading")
    b = Annotation(24, 600, "table")
    c = Annotation(51, 56, "tableheading")

    assert b > b
    assert a < c
    assert b < c


def test_sorting():
    annotations = [
        Annotation(24, 62, "tableheading"),
        Annotation(24, 600, "table"),
        Annotation(51, 56, "tableheading"),
        Annotation(59, 115, "tableheading"),
        Annotation(79, 104, "emphasis"),
        Annotation(125, 139, "tableheading"),
        Annotation(140, 160, "emphasis"),
        Annotation(254, 263, "link"),
        Annotation(254, 271, "bold"),
        Annotation(266, 268, "link"),
        Annotation(271, 280, "link"),
        Annotation(369, 385, "link"),
        Annotation(484, 498, "link"),
    ]

    assert sorted(annotations) == [
        Annotation(24, 600, "table"),
        Annotation(24, 62, "tableheading"),
        Annotation(51, 56, "tableheading"),
        Annotation(59, 115, "tableheading"),
        Annotation(79, 104, "emphasis"),
        Annotation(125, 139, "tableheading"),
        Annotation(140, 160, "emphasis"),
        Annotation(254, 271, "bold"),
        Annotation(254, 263, "link"),
        Annotation(266, 268, "link"),
        Annotation(271, 280, "link"),
        Annotation(369, 385, "link"),
        Annotation(484, 498, "link"),
    ]

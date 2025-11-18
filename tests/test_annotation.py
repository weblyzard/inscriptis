#!/usr/bin/env python

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
        a, content_width=5, line_width=10, align=HorizontalAlignment.left, shift=0,
    ).pop() == Annotation(0, 4, "test")

    # shift
    assert horizontal_shift(
        a, content_width=5, line_width=10, align=HorizontalAlignment.left, shift=3,
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

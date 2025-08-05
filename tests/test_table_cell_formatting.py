#!/usr/bin/env python

"""
Tests the Table formatting with different parameters such as width and
alignment
"""

from inscriptis.html_properties import HorizontalAlignment, VerticalAlignment
from inscriptis.model.table import TableCell


def test_horizontal_cell_formatting():
    cell = TableCell(align=HorizontalAlignment.left, valign=VerticalAlignment.top)
    # left alignment
    cell.blocks = ["Ehre sei Gott!"]
    cell.width = 16
    assert cell.blocks == ["Ehre sei Gott!  "]

    # right alignment
    cell.align = HorizontalAlignment.right
    cell.blocks = ["Ehre sei Gott!"]
    cell.width = 16
    assert cell.blocks == ["  Ehre sei Gott!"]


def test_vertical_cell_formatting():
    cell = TableCell(align=HorizontalAlignment.left, valign=VerticalAlignment.top)

    # default top alignment
    cell.blocks = ["Ehre sei Gott!"]
    cell.width = 16
    cell.height = 4
    assert cell.blocks == ["Ehre sei Gott!  ", "", "", ""]

    # bottom alignment
    cell.blocks = ["Ehre sei Gott!"]
    cell.valign = VerticalAlignment.bottom
    cell.width = 16
    cell.height = 4
    assert cell.blocks == ["", "", "", "Ehre sei Gott!  "]

    # middle alignment
    cell.blocks = ["Ehre sei Gott!"]
    cell.valign = VerticalAlignment.middle
    cell.width = 16
    cell.height = 4
    assert cell.blocks == ["", "Ehre sei Gott!  ", "", ""]

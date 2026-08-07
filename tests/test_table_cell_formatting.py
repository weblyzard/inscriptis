#!/usr/bin/env python

"""
Tests the Table formatting with different parameters such as width and
alignment
"""

from inscriptis.html_properties import HorizontalAlignment, VerticalAlignment
from inscriptis.model.table import TableCell


def test_horizontal_cell_formatting():
    # left alignment
    cell = TableCell(align=HorizontalAlignment.left, valign=VerticalAlignment.top)
    cell.blocks = ["Ehre sei Gott!"]
    cell.normalize_blocks()
    cell.width = 16
    assert list(cell.blocks) == ["Ehre sei Gott!  "]

    # right alignment
    cell = TableCell(align=HorizontalAlignment.left, valign=VerticalAlignment.top)
    cell.align = HorizontalAlignment.right
    cell.blocks = ["Ehre sei Gott!"]
    cell.normalize_blocks()
    cell.width = 16
    assert list(cell.blocks) == ["  Ehre sei Gott!"]


def test_vertical_cell_formatting():

    # default top alignment
    cell = TableCell(align=HorizontalAlignment.left, valign=VerticalAlignment.top)
    cell.blocks = ["Ehre sei Gott!", "In der Höhe"]
    cell.normalize_blocks()
    cell.height = 4
    assert list(cell.blocks) == ["Ehre sei Gott!", "In der Höhe   ", "              ", "              "]

    # bottom alignment
    cell = TableCell(align=HorizontalAlignment.left, valign=VerticalAlignment.top)
    cell.blocks = ["Ehre sei Gott!"]
    cell.normalize_blocks()
    cell.valign = VerticalAlignment.bottom
    cell.height = 4
    assert list(cell.blocks) == ["              ", "              ", "              ", "Ehre sei Gott!"]

    # middle alignment
    cell = TableCell(align=HorizontalAlignment.left, valign=VerticalAlignment.top)
    cell.blocks = ["Ehre sei Gott!"]
    cell.normalize_blocks()
    cell.valign = VerticalAlignment.middle
    cell.height = 4
    assert list(cell.blocks) == ["              ", "Ehre sei Gott!", "              ", "              "]


def test_horizontal_and_vertical_cell_formatting():
    """Check whether the vertical and horizontal padding are correct."""

    # default top alignment
    cell = TableCell(align=HorizontalAlignment.left, valign=VerticalAlignment.top)
    cell.blocks = ["Ehre sei Gott!"]
    cell.normalize_blocks()
    cell.width = 16
    cell.height = 4
    assert list(cell.blocks) == ["Ehre sei Gott!  ", "                ", "                ", "                "]

    # bottom alignment
    cell = TableCell(align=HorizontalAlignment.left, valign=VerticalAlignment.top)
    cell.blocks = ["Ehre sei Gott!"]
    cell.normalize_blocks()
    cell.valign = VerticalAlignment.bottom
    cell.width = 16
    cell.height = 4
    assert list(cell.blocks) == ["                ", "                ", "                ", "Ehre sei Gott!  "]

    # middle alignment
    cell = TableCell(align=HorizontalAlignment.left, valign=VerticalAlignment.top)
    cell.blocks = ["Ehre sei Gott!"]
    cell.normalize_blocks()
    cell.valign = VerticalAlignment.middle
    cell.width = 16
    cell.height = 4
    assert list(cell.blocks) == ["                ", "Ehre sei Gott!  ", "                ", "                "]

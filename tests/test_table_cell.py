#!/usr/bin/env python

"""
Tests the Table formatting with different parameters such as width and
alignment
"""

from inscriptis.html_properties import HorizontalAlignment, VerticalAlignment
from inscriptis.model.table import TableCell


def test_height():
    cell = TableCell(HorizontalAlignment.left, VerticalAlignment.top)

    cell.blocks = ["hallo"]
    cell.normalize_blocks()
    assert cell.height == len("\n".join(cell.blocks).split("\n"))

    cell.blocks = ["hallo", "echo"]
    cell.normalize_blocks()
    assert cell.height == 2

    cell.blocks = ["hallo\necho"]
    cell.normalize_blocks()
    assert cell.height == 2

    cell.blocks = ["hallo\necho", "Ehre sei Gott", "Jump\n&\nRun!\n\n\n"]
    cell.normalize_blocks()
    assert cell.height == 9
    assert cell.height == len("\n".join(cell.blocks).split("\n"))


def test_width():
    cell = TableCell(HorizontalAlignment.left, VerticalAlignment.top)

    cell.blocks = ["hallo"]
    cell.normalize_blocks()
    assert cell.width == len(cell.blocks[0])

    cell.blocks = ["hallo\necho", "Ehre sei Gott", "Jump\n&\nRun!\n\n\n"]
    cell.normalize_blocks()
    assert cell.width == len("Ehre sei Gott")

    # fixed set width
    cell.width = 95
    cell.normalize_blocks()
    assert cell.width == 95


def test_explicit_zero_width_is_preserved():
    cell = TableCell(HorizontalAlignment.left, VerticalAlignment.top)
    cell.blocks = [""]
    cell.normalize_blocks()

    assert cell.width == 0


def test_height_setter_rebuilds_from_content_blocks():
    cell = TableCell(HorizontalAlignment.left, VerticalAlignment.top)
    cell.blocks = ["a", "b"]
    cell.normalize_blocks()

    cell.height = 5
    cell.height = 4

    assert cell.blocks == ["a", "b", "", ""]
    assert cell.vertical_padding == 0


def test_empty_cell():
    cell = TableCell(HorizontalAlignment.left, VerticalAlignment.top)
    cell.blocks = []
    cell.normalize_blocks()

    assert cell.height == 1
    assert cell.width == 0

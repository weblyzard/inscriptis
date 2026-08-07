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


def test_line_width_is_cached():
    cell = TableCell(HorizontalAlignment.left, VerticalAlignment.top)
    cell.blocks = ["hallo\necho", "Ehre sei Gott"]
    cell.normalize_blocks()

    first = cell._line_width
    second = cell._line_width

    assert first is second

    # changes of the cell's width do not affect the cached line_width
    cell.width = 95
    assert first is second

    # changes to height do
    cell.height = 22
    assert first != cell._line_width
    assert len(cell._line_width) == 22


#!/usr/bin/env python

"""
Tests the Table formatting with different parameters such as width and
alignment
"""

import pytest

from inscriptis.html_properties import HorizontalAlignment, VerticalAlignment
from inscriptis.model.table import TableCell


def test_height():
    cell = TableCell(HorizontalAlignment.left, VerticalAlignment.top)
    cell.blocks = ["hallo"]
    cell.normalize_blocks()
    assert cell.height == len("\n".join(cell.blocks).split("\n"))

    cell = TableCell(HorizontalAlignment.left, VerticalAlignment.top)
    cell.blocks = ["hallo", "echo"]
    cell.normalize_blocks()
    assert cell.height == 2

    cell = TableCell(HorizontalAlignment.left, VerticalAlignment.top)
    cell.blocks = ["hallo\necho"]
    cell.normalize_blocks()
    assert cell.height == 2

    cell = TableCell(HorizontalAlignment.left, VerticalAlignment.top)
    cell.blocks = ["hallo\necho", "Ehre sei Gott", "Jump\n&\nRun!\n\n\n"]
    cell.normalize_blocks()
    assert cell.height == 9
    assert cell.height == len("\n".join(cell.blocks).split("\n"))


def test_width():
    cell = TableCell(HorizontalAlignment.left, VerticalAlignment.top)
    cell.blocks = ["hallo"]
    cell.normalize_blocks()
    assert cell.width == len(cell.blocks[0])

    cell = TableCell(HorizontalAlignment.left, VerticalAlignment.top)
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


def test_formatted_blocks_are_cached_as_tuple():
    cell = TableCell(HorizontalAlignment.left, VerticalAlignment.top)
    cell.blocks = ["hallo", "echo"]
    cell.normalize_blocks()
    cell.width = 6

    formatted_blocks = cell._formatted_blocks

    assert isinstance(formatted_blocks, tuple)
    assert formatted_blocks is cell._formatted_blocks


def test_width_is_enforced_to_be_at_least_content_width():
    cell = TableCell(HorizontalAlignment.left, VerticalAlignment.top)
    cell.blocks = ["hallo", "echo"]
    cell.normalize_blocks()

    with pytest.raises(ValueError, 
                       match="Cannot set cell width to 2 as it is smaller than the content's width of 5."):
        cell.width = 2

#!/usr/bin/env python
# encoding: utf-8

"""
Tests the Table formatting with different parameters such as width and
alignment
"""

from inscriptis.model.table import TableCell
from inscriptis.html_properties import HorizontalAlignment, VerticalAlignment


def test_horizontal_cell_formatting():

    canvas = []
    cell = TableCell(canvas=canvas, align=HorizontalAlignment.left,
                     valign=VerticalAlignment.top)
    cell.width = 16
    canvas.append('Ehre sei Gott!')

    # left alignment
    assert cell.get_cell_lines() == ['Ehre sei Gott!  ']

    # right alignment
    cell.align = HorizontalAlignment.right
    assert cell.get_cell_lines() == ['  Ehre sei Gott!']


def test_vertical_cell_formatting():
    canvas = []
    cell = TableCell(canvas=canvas, align=HorizontalAlignment.left,
                     valign=VerticalAlignment.top)
    cell.width = 16
    cell.height = 4
    canvas.append('Ehre sei Gott!')

    # default top alignment
    assert cell.get_cell_lines() == ['Ehre sei Gott!  ',
                                     '                ',
                                     '                ',
                                     '                ']

    # bottom alignment
    cell.valign = VerticalAlignment.bottom
    assert cell.get_cell_lines() == ['                ',
                                     '                ',
                                     '                ',
                                     'Ehre sei Gott!  ']

    # middle alignment
    cell.valign = VerticalAlignment.middle
    print(cell.get_cell_lines())
    assert cell.get_cell_lines() == ['                ',
                                     'Ehre sei Gott!  ',
                                     '                ',
                                     '                ']

#!/usr/bin/env python
# encoding: utf-8

'''
Tests the Table formatting with different parameters such as width and
alignment
'''

from inscriptis.model.table import TableCell
from inscriptis.html_properties import HorizontalAlignment


def test_cell_formatting():

    canvas = []
    cell = TableCell(canvas=canvas, align=HorizontalAlignment.left)
    cell.width = 16
    canvas.append('Ehre sei Gott!')

    # left alignment
    assert cell.get_cell_lines() == ['Ehre sei Gott!  ']

    # right alignment
    cell.align = HorizontalAlignment.right
    assert cell.get_cell_lines() == ['  Ehre sei Gott!']

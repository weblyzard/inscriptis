#!/usr/bin/env python
# encoding: utf-8

'''
test the line formatting with different parameters such as width and alignment
'''

from inscriptis.table_engine import TableCell

def test_cell_formatting():

    canvas = []
    cell = TableCell(canvas=canvas, align='<')
    cell.width = 16
    canvas.append('Ehre sei Gott!')

    # left alignment
    assert cell.get_cell_lines() == ['Ehre sei Gott!  ']

    # right alignment
    cell.align = '>'
    assert cell.get_cell_lines() == ['  Ehre sei Gott!']



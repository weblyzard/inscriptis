#!/usr/bin/env python
# encoding: utf-8

'''
test the line formatting with different parameters such as width and alignment
'''

from inscriptis.html_properties import Line

def test_line_formatting():

    line = Line()
    line.align = '<'
    line.width = 16
    line.content = 'Ehre sei Gott!'

    # left alignment
    assert line.get_text() == 'Ehre sei Gott!  '

    # right alignment
    line.align = '>'
    assert line.get_text() == '  Ehre sei Gott!'



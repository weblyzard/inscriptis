#!/usr/bin/env python
# encoding: utf-8

"""
Tests the rendering of a single table line.
"""

from inscriptis.model.canvas import Line


def test_cell_formatting():
    # standard line
    line = Line()
    line.margin_before = 0
    line.margin_after = 0
    line.prefix = ''
    line.suffix = ''
    line.content = 'Ehre sei Gott!'
    line.list_bullet = ''
    line.padding = 0

    assert line.get_text() == 'Ehre sei Gott!'
    # string representation
    assert str(line) == \
        "<Line: 'Ehre sei Gott!'>"
    assert repr(line) == str(line)

    # add margins
    line.margin_before = 1
    line.margin_after = 2
    assert line.get_text() == '\nEhre sei Gott!\n\n'

    # list bullet without padding
    line.list_bullet = "* "
    assert line.get_text() == '\n* Ehre sei Gott!\n\n'

    # add a padding
    line.padding = 3
    assert line.get_text() == '\n * Ehre sei Gott!\n\n'

    # and prefixes + suffixes
    line.prefix = '>>'
    line.suffix = '<<'
    assert line.get_text() == '\n * >>Ehre sei Gott!<<\n\n'

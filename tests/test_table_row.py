#!/usr/bin/env python
# encoding: utf-8

"""
Test borderline cases for table rows
"""

from inscriptis.model.table import TableRow

def test_empty_row():
    tr = TableRow()

    assert tr.width == 0
    assert tr.get_text() == ''

#!/usr/bin/env python

"""
Test borderline cases for table rows
"""

from inscriptis import get_text
from inscriptis.model.config import ParserConfig
from inscriptis.model.table import TableRow


def test_empty_row():
    tr = TableRow(cell_separator="   ")

    assert tr.width == 0
    assert tr.get_text() == ""


def test_table_cell_separator():
    html = "<html><body><table><tr><td>Hallo<br>Eins</td><td>Echo<br>Zwei</td></tr></table></html>"

    config = ParserConfig()
    assert get_text(html, config) == "Hallo  Echo\nEins   Zwei\n"

    config = ParserConfig(table_cell_separator="\t")
    assert get_text(html, config) == "Hallo\tEcho\nEins \tZwei\n"

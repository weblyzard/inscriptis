#!/usr/bin/env python
# encoding: utf-8

"""
Tests the handling of tables that do not properly close all column tags.
"""

from inscriptis.engine import get_text
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

config = ParserConfig(css=CSS_PROFILES['strict'])


def test_forgotten_td_close_tag():
    # one line (i.e., missing </td> before the next <td> and the next </tr>
    html = (u'<body>hallo<table>'
            '<tr><td>1<td>2</tr>'
            u'</table>echo</body>')
    assert get_text(html, config) == u'hallo\n1  2\necho'

    # two lines (i.e. missing </td> before the <tr> and before the </table>
    html = (u'<body>hallo<table>'
            '<tr><td>1<td>2'
            '<tr><td>3<td>4'
            u'</table>echo</body>')
    assert get_text(html, config) == u'hallo\n1  2\n3  4\necho'

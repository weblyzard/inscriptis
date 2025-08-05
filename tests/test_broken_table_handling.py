#!/usr/bin/env python

"""
Tests the handling of tables that do not properly close all column tags.
"""

from inscriptis import get_text
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

config = ParserConfig(css=CSS_PROFILES["strict"])


def test_forgotten_td_close_tag():
    # one line (i.e., missing </td> before the next <td> and the next </tr>
    html = "<body>hallo<table><tr><td>1<td>2</tr></table>echo</body>"
    print(html)
    # assert get_text(html, config) == u'hallo\n1  2\necho'

    # two lines (i.e. missing </td> before the <tr> and before the </table>
    html = "<body>hallo<table><tr><td>1<td>2<tr><td>3<td>4</table>echo</body>"
    print(html)
    assert get_text(html, config) == "hallo\n1  2\n3  4\n\necho"

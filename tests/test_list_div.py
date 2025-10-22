#!/usr/bin/env python

"""ensures that two successive <a>text</a> contain
a space between each other, if there is a linebreak
or space between the tags.
"""

from inscriptis import get_text
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

config = ParserConfig(css=CSS_PROFILES["strict"])


def test_divs():
    html = "<body>Thomas<div>Anton</div>Maria</body>"
    assert get_text(html, config) == "Thomas\nAnton\nMaria"

    html = "<body>Thomas<div>Anna <b>läuft</b> weit weg.</div>"
    assert get_text(html, config) == "Thomas\nAnna läuft weit weg."

    html = "<body>Thomas <ul><li><div>Anton</div>Maria</ul></body>"
    assert get_text(html, config) == "Thomas\n  * Anton\n    Maria"

    html = "<body>Thomas <ul><li>  <div>Anton</div>Maria</ul></body>"
    assert get_text(html, config) == "Thomas\n  * Anton\n    Maria"

    html = "<body>Thomas <ul><li> a  <div>Anton</div>Maria</ul></body>"
    assert get_text(html, config) == "Thomas\n  * a\n    Anton\n    Maria"

    html = "<body>Thomas <ol><li> a  <div>Anton</div>Maria</ol></body>"
    assert get_text(html, config) == "Thomas\n 1. a\n    Anton\n    Maria"

    html = """<body>Thomas <ol><li value="2"> a  <div>Anton</div>Maria</ol></body>"""
    assert get_text(html, config) == "Thomas\n 2. a\n    Anton\n    Maria"

    html = """<body>Thomas <ol><li value="2"> a  <ol><li><div>Anton</div></li></ol>Maria</ol></body>"""
    assert get_text(html, config) == "Thomas\n 2. a\n     1. Anton\n    Maria"

    html = """<body>Thomas <ol><li value="2"> a  <ol><li value="10"><div>Anton</div></li></ol>Maria</ol></body>"""
    assert get_text(html, config) == "Thomas\n 2. a\n    10. Anton\n    Maria"

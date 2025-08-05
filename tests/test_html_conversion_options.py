#!/usr/bin/env python

"""
Tests different HTML to text conversion options.
"""

from inscriptis import get_text
from inscriptis.model.config import ParserConfig


def test_display_links():
    html = """<html>
                 <body>
                   <a href="first">first</a>
                   <a href="second">second</a>
                   <a name="third">third</a>
                 </body>
                </html>
            """
    config = ParserConfig(display_links=True)
    assert get_text(html, config).strip() == "[first](first) [second](second) third"


def test_display_anchors():
    html = """<html>
                 <body>
                   <a name="first">first</a>
                   <a href="second">second</a>
                 </body>
                </html>
            """
    config = ParserConfig(display_anchors=True)
    assert get_text(html, config).strip() == "[first](first) second"


def test_display_links_and_anchors():
    html = """<html>
                 <body>
                   <a href="first">first</a>
                   <a href="second">second</a>
                   <a name="third">third</a>
                 </body>
                </html>
            """
    config = ParserConfig(display_links=True, display_anchors=True)
    assert get_text(html, config).strip() == "[first](first) [second](second) [third](third)"


def test_display_images():
    html = """<html>
                 <body>
                   <img src="test1" alt="Ein Test Bild" title="Hallo" />
                   <img src="test2" alt="Ein Test Bild" title="Juhu" />
                   <img src="test3" alt="Ein zweites Bild" title="Echo" />
                 </body>
                </html>
            """
    config = ParserConfig(display_images=True)
    assert get_text(html, config).strip() == "[Ein Test Bild] [Ein Test Bild] [Ein zweites Bild]"


def test_display_images_deduplicated():
    html = """<html>
                 <body>
                   <img src="test1" alt="Ein Test Bild" title="Hallo" />
                   <img src="test2" alt="Ein Test Bild" title="Juhu" />
                   <img src="test3" alt="Ein zweites Bild" title="Echo" />
                 </body>
                </html>
            """
    config = ParserConfig(display_images=True, deduplicate_captions=True)
    assert get_text(html, config).strip() == "[Ein Test Bild] [Ein zweites Bild]"

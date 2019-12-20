#!/usr/bin/env python

'''
Tests different HTML to text conversion options.
'''

from inscriptis import get_text


def test_display_links():
    html = '''<html>
                 <body>
                   <a href="first">first</a>
                   <a href="second">second</a>
                 </body>
                </html>
            '''
    assert get_text(html, display_links=True).strip() == \
        '[first](first) [second](second)'


def test_display_images():
    html = '''<html>
                 <body>
                   <img src="test1" alt="Ein Test Bild" title="Hallo" />
                   <img src="test2" alt="Ein Test Bild" title="Juhu" />
                   <img src="test3" alt="Ein zweites Bild" title="Echo" />
                 </body>
                </html>
            '''
    assert get_text(html, display_images=True).strip() == \
        '[Ein Test Bild] [Ein Test Bild] [Ein zweites Bild]'


def test_display_images_deduplicated():
    html = '''<html>
                 <body>
                   <img src="test1" alt="Ein Test Bild" title="Hallo" />
                   <img src="test2" alt="Ein Test Bild" title="Juhu" />
                   <img src="test3" alt="Ein zweites Bild" title="Echo" />
                 </body>
                </html>
            '''
    assert get_text(html, display_images=True,
                    deduplicate_captions=True).strip() == \
        '[Ein Test Bild] [Ein zweites Bild]'

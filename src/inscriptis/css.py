#!/usr/bin/env python
# coding: utf-8

'''
Handeling of CSS files.
'''

from collections import namedtuple
from inscriptis.html import Display, WhiteSpace

HtmlElement = namedtuple("HtmlElement", "tag prefix suffix display margin_before margin_after padding whitespace")
HtmlElement.__new__.__defaults__ = ('/', '', '', Display.inline, 0, 0, 0, WhiteSpace.normal)

CSS = {
    'head': HtmlElement('head', display=Display.none),
    'link': HtmlElement('link', display=Display.none),
    'meta': HtmlElement('meta', display=Display.none),
    'script': HtmlElement('script', display=Display.none),
    'title': HtmlElement('title', display=Display.none),

    'p': HtmlElement('p', display=Display.block, margin_before=1, margin_after=1),
    'figure': HtmlElement('figure', display=Display.block, margin_before=1, margin_after=1),

    'ul': HtmlElement('ul', display=Display.block, margin_before=1, margin_after=1, padding=4),
    'ol': HtmlElement('ol', display=Display.block, margin_before=1, margin_after=1, padding=4),

    'address': HtmlElement('address', display=Display.block),
    'article': HtmlElement('article', display=Display.block),
    'aside': HtmlElement('aside', display=Display.block),
    'div': HtmlElement('div', display=Display.block),
    'footer': HtmlElement('footer', display=Display.block),
    'header': HtmlElement('header', display=Display.block),
    'hgroup': HtmlElement('hgroup', display=Display.block),
    'layer': HtmlElement('layer', display=Display.block),
    'main': HtmlElement('main', display=Display.block),
    'nav': HtmlElement('nav', display=Display.block),
    'figcaption': HtmlElement('figcaption', display=Display.block),

    'blockquote': HtmlElement('blockquote', display=Display.block),

    'q': HtmlElement('q', prefix='"', suffix='"'),
    'span': HtmlElement('span', ),
}

#!/usr/bin/env python
# coding: utf-8

'''
Handeling of CSS files.
'''

from collections import namedtuple
from inscriptis.html_properties import Display, WhiteSpace

HtmlElement = namedtuple("HtmlElement", "tag prefix suffix display margin_before margin_after padding whitespace")
HtmlElement.__new__.__defaults__ = ('/', '', '', Display.inline, 0, 0, 0, WhiteSpace.normal)

CSS = {
    'head': HtmlElement('head', display=Display.none),
    'link': HtmlElement('link', display=Display.none),
    'meta': HtmlElement('meta', display=Display.none),
    'script': HtmlElement('script', display=Display.none),
    'title': HtmlElement('title', display=Display.none),
    'style': HtmlElement('style', display=Display.none),

    'p': HtmlElement('p', display=Display.block, margin_before=1, margin_after=1),
    'figure': HtmlElement('figure', display=Display.block, margin_before=1, margin_after=1),


    'h1': HtmlElement('h1', display=Display.block, margin_before=1, margin_after=1),
    'h2': HtmlElement('h2', display=Display.block, margin_before=1, margin_after=1),
    'h3': HtmlElement('h3', display=Display.block, margin_before=1, margin_after=1),
    'h4': HtmlElement('h4', display=Display.block, margin_before=1, margin_after=1),
    'h5': HtmlElement('h5', display=Display.block, margin_before=1, margin_after=1),
    'h6': HtmlElement('h6', display=Display.block, margin_before=1, margin_after=1),

    'ul': HtmlElement('ul', display=Display.block, margin_before=0, margin_after=0, padding=4),
    'ol': HtmlElement('ol', display=Display.block, margin_before=0, margin_after=0, padding=4),
    'li': HtmlElement('li', display=Display.block),

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

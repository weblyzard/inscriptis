#!/usr/bin/env python3
# encoding: utf-8

'''
This module provides the following properties for the
:class:`inscriptis.css.HtmlElement`.

 1. :class:`Display` properites.
 2. :class:`WhiteSpace` properties.
 3. the :class:`Line` element that determines how a single line is rendered.
'''


class Display(object):
    '''
    This class specifies whether content will be rendered as inline, block or
    none (i.e. not rendered).
    '''
    inline = 1
    block = 2
    none = 3


class WhiteSpace(object):
    '''
    This class specifies the whitespace handling used for an HTML element as
    outlined in the `Cascading Style Sheets <https://www.w3.org/TR/CSS1/>`_
    specification.

    .. data:: normal

    Sequences of whitespaces will be collapsed into a single one.

    .. data:: pre

    Sequences of whitespaces will preserved.
    '''
    normal = 1
    pre = 3


class Line(object):
    '''
    This class represents a line to render.
    '''
    __slots__ = ('margin_before', 'margin_after', 'prefix', 'suffix',
                 'content', 'list_bullet', 'padding', 'align', 'width')

    def __init__(self):
        self.margin_before = 0
        self.margin_after = 0
        self.prefix = ""
        self.suffix = ""
        self.content = ""
        self.list_bullet = ""
        self.padding = 0

    def extract_pre_text(self):
        pass

    def get_text(self):
        '''
        Returns:
          str -- The text representation of the current line.
        '''
        return ''.join(('\n' * self.margin_before,
                        ' ' * (self.padding - len(self.list_bullet)),
                        self.list_bullet,
                        self.prefix,
                        ' '.join(self.content.split()),
                        self.suffix,
                        '\n' * self.margin_after))

    def __str__(self):
        return f"<Line: '{self.get_text().strip()}'>"

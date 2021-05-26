#!/usr/bin/env python
# encoding: utf-8

"""
Elements used for rendering (parts) of the canvas.

The :class:`Line` determines how a single line is rendered.
"""
from html import unescape

from inscriptis.model.css import HtmlElement


class Canvas:
    """
    The Canvas on which we write our HTML page.
    """

    def __init__(self):
        self.blocks = []
        self.indent = ''
        self.head = ''
        self.tail = ''

    def write_block(self, tag: HtmlElement, text: str):
        self.flush_inline()
        self.head = text

    def write_inline(self, tag: HtmlElement, text: str):
        self.tail += text

    def flush_inline(self):
        if self.head or self.tail:
            self.blocks.append(self.head + ' '.join(self.tail.split()))
            self.indent = ''
            self.head = ''
            self.tail = ''

    def get_text(self):
        self.flush_inline()
        return unescape('\n'.join((block.rstrip() for block in self.blocks)))
        # return text if not text.startswith('\n') else text[1:]


class Line:
    """
    This class represents a line to render.

    Args:
        margin_before: number of empty lines before the given line.
        margin_after: number of empty lines before the given line.
        prefix: prefix add before the line's content.
        suffix: suffix to add after the line's content.
        list_bullet: a bullet to add before the line.
        padding: horizontal padding
        align: determines the alignment of the line (not used yet)
        width: total width of the line in characters (not used yet)
    """
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

    def get_text(self):
        """
        Returns:
          str -- The text representation of the current line.
        """
        if '\0' not in self.content:
            # standard text without any `WhiteSpace.pre` formatted text.
            text = self.content.split()
        else:
            # content containing `WhiteSpace.pre` formatted text
            self.content = self.content.replace('\0\0', '')
            text = []
            # optional padding to add before every line
            base_padding = ' ' * self.padding

            for no, data in enumerate(self.content.split('\0')):
                # handle standard content
                if no % 2 == 0:
                    text.extend(data.split())
                # handle `WhiteSpace.pre` formatted content.
                else:
                    text.append(data.replace('\n', '\n' + base_padding))

        return ''.join(('\n' * self.margin_before,
                        ' ' * (self.padding - len(self.list_bullet)),
                        self.list_bullet,
                        self.prefix,
                        ' '.join(text),
                        self.suffix,
                        '\n' * self.margin_after))

    def __str__(self):
        return "<Line: '{0}'>".format(self.get_text())

    def __repr__(self):
        return str(self)

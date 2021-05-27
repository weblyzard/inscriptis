#!/usr/bin/env python
# encoding: utf-8

"""
Elements used for rendering (parts) of the canvas.

The :class:`Line` determines how a single line is rendered.
"""
from collections import namedtuple
from enum import Enum
from html import unescape

from inscriptis.html_properties import WhiteSpace
from inscriptis.model.css import HtmlElement

TextSnippet = namedtuple("TextSnippet", "text whitespace")


class Canvas:
    """
    The Canvas on which we write our HTML page.
    """

    def __init__(self):
        """
        Contains the completed blocks. Each block spawns at least a line
        """
        self.blocks = []
        self.current_block = []

    def write_block(self, tag: HtmlElement, text: str):
        self.flush_inline()
        self.current_block.append(TextSnippet(text, whitespace=0))

    def write_inline(self, tag: HtmlElement, text: str):
        if tag.whitespace == WhiteSpace.pre:
            self.current_block.append(TextSnippet(text, whitespace=0))
        else:
            space_handling = 1 + 2 * text[0].isspace() + 4 * (text[-1].isspace() and len(text) > 1)
            self.current_block.append(TextSnippet(text, whitespace=space_handling))

    @staticmethod
    def normalize_text(text_snippet):
        return ''.join((' ' if (text_snippet.whitespace & 2) else '',
                        ' '.join(text_snippet.text.split()),
                        ' ' if (text_snippet.whitespace & 4) else ''))

    def flush_inline(self):
        if self.current_block:
            print(self.current_block)
            block = ''.join((self.normalize_text(b) if b.whitespace else b.text
                             for b in self.current_block))
            self.blocks.append(block)
            self.current_block = []

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

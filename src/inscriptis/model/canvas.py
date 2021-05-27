#!/usr/bin/env python
# encoding: utf-8

"""
Elements used for rendering (parts) of the canvas.

The :class:`Canvas` represents the drawing board to which the HTML page
is serialized.
"""
from collections import namedtuple
from html import unescape

from inscriptis.html_properties import WhiteSpace
from inscriptis.model.html_element import HtmlElement

TextSnippet = namedtuple("TextSnippet", "text whitespace")


class Canvas:
    """
    The Canvas on which we write our HTML page.
    """

    __slots__ = ('blocks', 'current_block', 'prefix')

    def __init__(self):
        """
        Contains the completed blocks. Each block spawns at least a line
        """
        self.prefix = []
        self.blocks = []
        self.current_block = []

    def write_block(self, tag: HtmlElement, text: str):
        self.flush_inline()
        self.prefix = [' ' * (tag.padding - len(tag.list_bullet)),
                       tag.list_bullet]
        self.current_block.append(TextSnippet(text, whitespace=WhiteSpace.pre))

    def write_inline(self, tag: HtmlElement, text: str):
        self.current_block.append(TextSnippet(text, whitespace=tag.whitespace))

    def _normalize(self, snippets: list[TextSnippet]):
        """Normalizes a list of TextSnippets to a single line

        Args:
            snippets: a list of TextSnippets

        Returns:
            the normalized string
        """
        result = self.prefix.copy()
        previous_isspace = False
        for snippet in snippets:
            # handling of pre formatted text
            if snippet.whitespace == WhiteSpace.pre:
                for line in snippet.text.split("\n"):
                    result.append(snippet.text)
                    result.extend(self.prefix)
                previous_isspace = None
                continue

            for ch in snippet.text:
                if not ch.isspace():
                    result.append(ch)
                    previous_isspace = False
                    continue

                if previous_isspace or not result:
                    continue
                else:
                    result.append(' ')
                    previous_isspace = True

        return ''.join(result)

    def flush_inline(self):
        if self.current_block:
            print(self.current_block)
            block = self._normalize(self.current_block)
            self.blocks.append(block)
            self.current_block = []

    def get_text(self):
        self.flush_inline()
        return unescape('\n'.join((block.rstrip() for block in self.blocks)))
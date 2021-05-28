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
    The text Canvas on which Inscriptis writes the HMTL page.
    """

    __slots__ = ('blocks', 'current_block', 'prefix', 'margin')

    def __init__(self):
        """
        Contains the completed blocks. Each block spawns at least a line
        """
        self.prefix = []
        self.blocks = []
        self.current_block = []
        self.margin = 1000  # margin to the previous block

    def write_block(self, tag: HtmlElement, text: str):
        self._flush_inline()

        # write the block margin
        required_margin = max(tag.previous_margin_after, tag.margin_before)
        if required_margin > self.margin:
            self.blocks.append('\n' * (required_margin - self.margin - 1))
        # print("\n\n", self.blocks, "\n", "WRITE: Required / current", tag, required_margin, self.margin)

        # write block content (considering its padding)
        self.prefix = [' ' * (tag.padding - len(tag.list_bullet)),
                       tag.list_bullet]
        self.current_block.append(TextSnippet(text, whitespace=tag.whitespace))

    def close_block(self, tag: HtmlElement):
        """
        Closes the given HtmlElement by writing its bottom margin.

        Args:
            tag: the HTML Block element to close
        """
        self._flush_inline()
        if tag.margin_after > self.margin:
            self.blocks.append('\n' * (tag.margin_after - self.margin - 1))
            # print("\n\n", self.blocks, "\n", "CLOSE: Required / current", tag, tag.margin_after, self.margin)
            self.margin = tag.margin_after

    def write_newline(self):
        self._flush_inline()
        self.blocks.append('')

    def write_inline(self, tag: HtmlElement, text: str):
        self.current_block.append(TextSnippet(text, whitespace=tag.whitespace))

    def get_text(self):
        """
        Provide a text representation of the current block
        """
        self._flush_inline()
        return unescape('\n'.join((block.rstrip(' ') for block in self.blocks)))

    def _normalize(self, snippets: list[TextSnippet]):
        """Normalizes a list of TextSnippets to a single line

        Args:
            snippets: a list of TextSnippets

        Returns:
            the normalized string representing the TextSnippets in the line
        """
        result = self.prefix
        # only keep the padding for further lines (i.e., remove bullets)
        self.prefix = [' ' * sum(map(len, self.prefix))]
        previous_isspace = True
        for snippet in snippets:
            # handling of pre formatted text
            if snippet.whitespace == WhiteSpace.pre:
                for line in snippet.text.split("\n"):
                    result.append(snippet.text)
                    result.extend(self.prefix)
                previous_isspace = result[-1].isspace()
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

    def _flush_inline(self):
        normalized_block = self._normalize(self.current_block)
        if normalized_block:
            print(".......................", self.current_block)
            self.blocks.append(normalized_block)
            self.current_block = []
            self.margin = 0

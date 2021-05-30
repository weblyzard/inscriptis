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

class Prefix:

    __slots__ = ('_padding_inline', '_bullet')

    def __init__(self, padding_inline, bullet):
        self._padding_inline = padding_inline
        self._bullet = bullet

    @property
    def padding(self):
        """
        Returns the padding for the given prefix.
        """
        return ' ' * self._padding_inline

    @property
    def bullet(self):
        b = self._bullet
        self._bullet = ''
        return b

    def __str__(self):
        return '"' + ' ' * (self._padding_inline - len(self._bullet)) + self._bullet + '"'

    __repr__ = __str__



class Canvas:
    """
    The text Canvas on which Inscriptis writes the HMTL page.
    """

    __slots__ = ('blocks', 'current_block', 'prefixes', 'margin')

    def __init__(self):
        """
        Contains the completed blocks. Each block spawns at least a line
        """
        self.prefixes = [Prefix(0, '')]
        self.blocks = []
        self.current_block = []
        self.margin = 1000  # margin to the previous block

    def open_block(self, tag: HtmlElement):
        """
        Opens an HTML block element.
        """
        self._flush_inline()
        self.prefixes.append(Prefix(tag.padding_inline, tag.list_bullet))

        # write the block margin
        required_margin = max(tag.previous_margin_after, tag.margin_before)
        if required_margin > self.margin:
            self.blocks.append('\n' * (required_margin - self.margin - 1))
            self.margin = required_margin

    def write(self, tag: HtmlElement, text: str, whitespace=None):
        """
        Writes the given block.
        """
        self.current_block.append(TextSnippet(text,
                                              whitespace=whitespace or tag.whitespace))

    def close_block(self, tag: HtmlElement):
        """
        Closes the given HtmlElement by writing its bottom margin.

        Args:
            tag: the HTML Block element to close
        """
        self._flush_inline()
        self.prefixes.pop()
        if tag.margin_after > self.margin:
            self.blocks.append('\n' * (tag.margin_after - self.margin - 1))
            self.margin = tag.margin_after

    def write_newline(self):
        if not self._flush_inline():
            self.blocks.append('')

    def get_text(self):
        """
        Provide a text representation of the current block
        """
        self._flush_inline()
        return unescape('\n'.join((block.rstrip(' ') for block in self.blocks)))

    def _flush_inline(self):
        normalized_block = self._normalize(self.current_block)
        if normalized_block:
            self.blocks.append(normalized_block)
            self.current_block = []
            self.margin = 0
            return True
        return False

    def _normalize(self, snippets: list[TextSnippet]):
        """Normalizes a list of TextSnippets to a single line

        Args:
            snippets: a list of TextSnippets

        Returns:
            the normalized string representing the TextSnippets in the line
        """
        result = []
        previous_isspace = True
        for snippet in snippets:
            # handling of pre formatted text
            if snippet.whitespace == WhiteSpace.pre:
                result.extend(snippet.text)
                previous_isspace = (result[-1] == '\n')
                continue

            # handling of inline text
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

        # does the textblock yield a result?
        block = ''.join(result)
        if not block:
            return

        subsequent_prefix = ''.join((p.padding for p in self.prefixes))
        bullet = ''.join((p.bullet for p in self.prefixes))
        if bullet:
            first_prefix = subsequent_prefix[:-len(bullet)] + bullet
        else:
            first_prefix = subsequent_prefix

        if block and first_prefix:
            block = first_prefix + block.replace('\n', '\n' + subsequent_prefix)
        return block

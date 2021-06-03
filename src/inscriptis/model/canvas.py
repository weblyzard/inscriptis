#!/usr/bin/env python
# encoding: utf-8

"""
Elements used for rendering (parts) of the canvas.

The :class:`Canvas` represents the drawing board to which the HTML page
is serialized.
"""
from html import unescape

from inscriptis.annotation import Annotation
from inscriptis.html_properties import WhiteSpace, Display
from inscriptis.model.block import Block
from inscriptis.model.html_element import HtmlElement
from inscriptis.model.prefix import Prefix


class Canvas:
    """
    The text Canvas on which Inscriptis writes the HTML page.

    Attributes:
        margin: the current margin to the previous block (this is required to
                ensure that the `margin_after` and `margin_before` constraints
                of HTML block elements are met).
        current_block: A list of TextSnippets that will be consolidated into a
                       block, once the current block is completed.
        blocks: a list of finished blocks (i.e., text lines)
        annotations: the list of completed annotations
        annotation_counter: a counter used for enumerating all annotations
                            we encounter.
        verbatim: indicates that we do not strip trailing whitespaces from
                  the content returned by the canvas (required for tables).
    """

    __slots__ = ('annotations', 'block_annotations', 'blocks', 'current_block',
                 'margin', 'annotation_counter', 'verbatim')

    def __init__(self, verbatim=False):
        """
        Contains the completed blocks. Each block spawns at least a line
        """
        self.margin = 1000  # margin to the previous block
        self.current_block = Block(0, Prefix(), verbatim)
        self.blocks = []
        self.annotations = []
        self.annotation_counter = {}
        self.block_annotations = {}

    def open_block(self, tag: HtmlElement):
        """
        Opens an HTML block element.
        """
        self._flush_inline()
        self.current_block.prefix.register_prefix(tag.padding_inline,
                                                  tag.list_bullet)

        # write the block margin
        required_margin = max(tag.previous_margin_after, tag.margin_before)
        if required_margin > self.margin:
            required_newlines = required_margin - self.margin
            self.current_block.idx += required_newlines
            self.blocks.append('\n' * (required_newlines - 1))
            self.margin = required_margin

        if tag.annotation:
            self.block_annotations[tag] = self.current_block.idx

    def write(self, tag: HtmlElement, text: str,
              whitespace: WhiteSpace = None):
        """
        Writes the given block.
        """
        span = self.current_block.merge(text, whitespace or tag.whitespace)

        if tag.annotation and tag.display != Display.block \
                and span.start != span.end:
            for annotation in tag.annotation:
                self.annotations.append(
                    Annotation(span.start, span.end, annotation))

    def close_block(self, tag: HtmlElement):
        """
        Closes the given HtmlElement by writing its bottom margin.

        Args:
            tag: the HTML Block element to close
        """

        flushed = self._flush_inline()
        self.current_block.prefix.remove_last_prefix()

        if tag in self.block_annotations:
            start_idx = self.block_annotations.pop(tag)
            end_idx = self.current_block.idx if not flushed \
                else self.current_block.idx - 1
            for annotation in tag.annotation:
                self.annotations.append(
                    Annotation(start_idx, end_idx, annotation))

        if tag.margin_after > self.margin:
            required_newlines = tag.margin_after - self.margin
            self.current_block.idx += required_newlines
            self.blocks.append('\n' * (required_newlines - 1))
            self.margin = tag.margin_after

    def write_newline(self):
        if not self._flush_inline():
            self.blocks.append('')
            self.current_block = self.current_block.new_block()

    def get_text(self) -> str:
        """
        Provide a text representation of the current block
        """
        self._flush_inline()
        return unescape('\n'.join(self.blocks))

    def _flush_inline(self) -> bool:
        """
        Attempts to flush the content in self.current_block into a new block
        which is added to self.blocks.

        If self.current_block does not contain any content (or only
        whitespaces) no changes are made.

        Returns: True if the attempt was successful, False otherwise.
        """
        if not self.current_block.is_empty():
            self.blocks.append(self.current_block.content)
            self.current_block = self.current_block.new_block()
            self.margin = 0
            return True

        return False

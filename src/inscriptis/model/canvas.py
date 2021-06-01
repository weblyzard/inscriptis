#!/usr/bin/env python
# encoding: utf-8

"""
Elements used for rendering (parts) of the canvas.

The :class:`Canvas` represents the drawing board to which the HTML page
is serialized.
"""
from collections import namedtuple
from contextlib import suppress
from html import unescape

from typing import List, Optional

from inscriptis.annotation import Annotation
from inscriptis.html_properties import WhiteSpace
from inscriptis.model.html_element import HtmlElement

TextSnippet = namedtuple('TextSnippet', 'text whitespace')


class Prefix:
    """Class Prefix manages paddings and bullets that prefix an HTML block.

    Note:
        In Inscriptis an HTML block corresponds to a line in the final output,
        since new blocks (Display.block) trigger line breaks while inline
        content (Display.normal) does not.

    Class variables:
        padding_inline: the number of characters used for padding_inline an
                        HTML block.
        bullet: an optional bullet used for padding_inline the HTML block.
    """

    __slots__ = ('current_padding', 'last_used_bullet', 'paddings', 'bullets',
                 'consumed')

    def __init__(self):
        self.current_padding = 0
        self.paddings = []
        self.bullets = []
        self.last_used_bullet = None
        self.consumed = False

    def register_prefix(self, padding_inline, bullet):
        """
        Registers the given prefix.
        Args:
            padding_inline: the number of characters used for padding_inline
            bullet: an optional bullet.
        """
        self.current_padding += padding_inline
        self.paddings.append(padding_inline)
        if bullet:
            self.bullets.append(bullet)

    def remove_last_prefix(self):
        """
        Remotes the last prefix from the list.
        """
        with suppress(IndexError):
            self.current_padding -= self.paddings.pop()
            del self.bullets[-1]

    def restore(self):
        """
        Restores the last_used_bullet, if present so that the iterator
        behaves like before.
        """
        if self.last_used_bullet:
            self.bullets.append(self.last_used_bullet)
            self.last_used_bullet = None

    def __iter__(self):
        self.consumed = False
        return self

    def __next__(self):
        if self.bullets and not self.consumed:
            self.consumed = True
            self.last_used_bullet = self.bullets.pop(0)
            return ' ' * (self.current_padding - len(self.last_used_bullet)) \
                   + self.last_used_bullet
        return ' ' * self.current_padding


class Canvas:
    """
    The text Canvas on which Inscriptis writes the HTML page.

    Attributes:
        prefixes: the list of prefixes (i.e., indentation and bullets) to be
                  considered when writing the block.
        margin: the current margin to the previous block (this is required to
                ensure that the `margin_after` and `margin_before` constraints
                of HTML block elements are met).
        current_block: A list of TextSnippets that will be consolidated into a
                       block, once the current block is completed.
        current_annotations: A list of annotations to maintain for
                             current_block
        blocks: a list of finished blocks (i.e., text lines)
        annotations: the list of completed annotations
        annotation_counter: a counter used for enumerating all annotations
                            we encounter.
        idx: the overall character index
        current_idx: the character index within the current block
    """

    __slots__ = ('annotations', 'blocks', 'current_annotations',
                 'current_block', 'prefixes', 'margin', 'annotation_counter',
                 'current_idx', 'idx')

    def __init__(self):
        """
        Contains the completed blocks. Each block spawns at least a line
        """
        self.prefixes = Prefix()
        self.margin = 1000  # margin to the previous block
        self.current_block = []
        self.current_annotations = []
        self.blocks = []
        self.idx = 0
        self.current_idx = 0
        self.annotations = []
        self.annotation_counter = {}

    def open_block(self, tag: HtmlElement):
        """
        Opens an HTML block element.
        """
        self._flush_inline()
        self.prefixes.register_prefix(tag.padding_inline, tag.list_bullet)

        # write the block margin
        required_margin = max(tag.previous_margin_after, tag.margin_before)
        if required_margin > self.margin:
            self.blocks.append('\n' * (required_margin - self.margin - 1))
            self.margin = required_margin
            self.current_idx += len(self.blocks[-1])

    def write(self, tag: HtmlElement, text: str,
              whitespace: WhiteSpace = None):
        """
        Writes the given block.
        """
        self.current_block.append(TextSnippet(
            text, whitespace=whitespace or tag.whitespace))
        # annotate content, if required
        text_len = len(text)

        if tag.annotation:
            for annotation in tag.annotation:
                self.current_annotations.append(
                    Annotation(self.current_idx, self.current_idx + text_len,
                               text, annotation))
        self.current_idx += text_len

    def close_block(self, tag: HtmlElement):
        """
        Closes the given HtmlElement by writing its bottom margin.

        Args:
            tag: the HTML Block element to close
        """
        self._flush_inline()
        self.prefixes.remove_last_prefix()
        if tag.margin_after > self.margin:
            self.blocks.append('\n' * (tag.margin_after - self.margin - 1))
            self.margin = tag.margin_after
            self.current_idx += len(self.blocks[-1])

    def write_newline(self):
        if not self._flush_inline():
            self.blocks.append('')
            self.idx += 1

    def get_text(self) -> str:
        """
        Provide a text representation of the current block
        """
        self._flush_inline()
        return unescape('\n'.join((block.rstrip(' ')
                                   for block in self.blocks)))

    def _flush_inline(self) -> bool:
        """
        Attempts to flush the content in self.current_block into a new block
        which is added to self.blocks.

        If self.current_block does not contain any content (or only
        whitespaces) no changes are made.

        Returns: True if the attempt was successful, False otherwise.
        """
        normalized_block = self._normalize(self.current_block)
        if normalized_block:
            self.blocks.append(normalized_block)
            self.idx += len(self.blocks[-1]) + 1   # +1 for the newline
            self.current_block = []
            self.margin = 0
            return True
        # only retain the last list element, if multiple blocks solely contain
        # collapsable whitespaces (i.e., normalize_block yields False).
        elif len(self.current_block) > 1:
            self.current_block = [self.current_block[-1]]
        return False

    def _normalize(self, snippets: List[TextSnippet]) -> Optional[str]:
        """Normalizes a list of TextSnippets to a single line

        Strategy:
        - pre-formatted text (WhiteSpace.pre) is added "as is".
        - for inline content (WhiteSpace.normal) all whitespaces are collapsed
        - finally, the prefix (padding_inline + bullets) is added to the
          content.

        Args:
            snippets: a list of TextSnippets

        Returns:
            the normalized string representing the TextSnippets in the line or
            None if the list does not contain any content.
        """
        content = []
        collapsed_whitespace_idx = []
        idx = 0
        previous_isspace = True
        for snippet in snippets:
            # handling of pre formatted text
            if snippet.whitespace == WhiteSpace.pre:
                content.extend(snippet.text)
                idx += len(snippet.text)
                previous_isspace = (content[-1] == '\n')
                continue

            # handling of inline text
            for idx, ch in enumerate(snippet.text, idx):
                if not ch.isspace():
                    content.append(ch)
                    previous_isspace = False
                    continue

                if previous_isspace or not content:
                    collapsed_whitespace_idx.append(idx)
                    continue
                else:
                    content.append(' ')
                    previous_isspace = True
            idx += 1

        # does the text block yield a result?
        block = ''.join(content)
        if not block:
            return

        for no, prefix in enumerate(self.prefixes):
            if no == 0:
                first_prefix = prefix
            elif no == 1:
                subsequent_prefix = prefix
            else:
                break

        if block and first_prefix:
            block = first_prefix + block.replace('\n',
                                                 '\n' + subsequent_prefix)
        return block

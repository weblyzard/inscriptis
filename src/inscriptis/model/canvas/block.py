"""Representation of a text block within the HTML canvas."""

from __future__ import annotations

from html import unescape
from typing import TYPE_CHECKING

from inscriptis.html_properties import WhiteSpace

if TYPE_CHECKING:
    from inscriptis.model.canvas import Prefix


class Block:
    """The current block of text.

    A block usually refers to one line of output text.

    .. note::
        If pre-formatted content is merged with a block, it may also contain
        multiple lines.

    Args:
        idx: the current block's start index.
        prefix: prefix used within the current block.

    """

    __slots__ = ("_content", "collapsable_whitespace", "idx", "prefix")

    def __init__(self, idx: int, prefix: Prefix):
        self.idx = idx
        self.prefix = prefix
        self._content = ""
        self.collapsable_whitespace = True

    def merge(self, text: str, whitespace: WhiteSpace) -> None:
        """Merge the given text with the current block.

        Args:
            text: the text to merge.
            whitespace: whitespace handling.

        """
        if whitespace == WhiteSpace.pre:
            self.merge_pre_text(text)
        else:
            self.merge_normal_text(text)

    def merge_normal_text(self, text: str) -> None:
        """Merge the given text with the current block.

        Args:
            text: the text to merge

        Note:
            If the previous text ended with a whitespace and text starts with one, both
             will automatically collapse into a single whitespace.

        """
        normalized_text = []

        for ch in text:
            if not ch.isspace():
                normalized_text.append(ch)
                self.collapsable_whitespace = False
            elif not self.collapsable_whitespace:
                normalized_text.append(" ")
                self.collapsable_whitespace = True

        if normalized_text:
            text = "".join((self.prefix.first, *normalized_text)) if not self._content else "".join(normalized_text)
            text = unescape(text)
            self._content += text
            self.idx += len(text)

    def merge_pre_text(self, text: str) -> None:
        """Merge the given pre-formatted text with the current block.

        Args:
            text: the text to merge

        """
        text = "".join((self.prefix.first, text.replace("\n", "\n" + self.prefix.rest)))
        text = unescape(text)
        self._content += text
        self.idx += len(text)
        self.collapsable_whitespace = False

    def is_empty(self) -> bool:
        return len(self.content) == 0

    @property
    def content(self):
        if not self.collapsable_whitespace:
            return self._content

        if self._content.endswith(" "):
            self._content = self._content[:-1]
            self.idx -= 1
        return self._content

    def new_block(self) -> Block:
        """Return a new Block based on the current one."""
        self.prefix.consumed = False
        return Block(idx=self.idx + 1, prefix=self.prefix)

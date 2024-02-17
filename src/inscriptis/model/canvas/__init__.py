#!/usr/bin/env python
# encoding: utf-8

"""Classes used for rendering (parts) of the canvas.

Every parsed :class:`~inscriptis.model.html_element.HtmlElement` writes its
textual content to the canvas which is managed by the following three classes:

  - :class:`Canvas` provides the drawing board on which the HTML page is
    serialized and annotations are recorded.
  - :class:`~inscriptis.model.canvas.block.Block` contains the current line to
    which text is written.
  - :class:`~inscriptis.model.canvas.prefix.Prefix` handles indentation
    and bullets that prefix a line.
"""

from inscriptis.annotation import Annotation
from inscriptis.html_properties import WhiteSpace, Display
from inscriptis.model.canvas.block import Block
from inscriptis.model.canvas.prefix import Prefix
from inscriptis.model.html_element import HtmlElement


class Canvas:
    r"""The text Canvas on which Inscriptis writes the HTML page.

    Attributes:
        margin: the current margin to the previous block (this is required to
            ensure that the `margin_after` and `margin_before` constraints of
            HTML block elements are met).
        current_block: A :class:`~inscriptis.model.canvas.block.Block` which
            merges the input text into a block (i.e., line).
        blocks: a list of strings containing the completed blocks (i.e.,
            text lines). Each block spawns at least one line.
        annotations: the list of recorded
            :class:`~inscriptis.annotation.Annotation`\s.
        _open_annotations: a map of open tags that contain annotations.
    """

    __slots__ = (
        "annotations",
        "blocks",
        "current_block",
        "_open_annotations",
        "margin",
    )

    def __init__(self):
        self.margin = 1000  # margin to the previous block
        self.current_block = Block(0, Prefix())
        self.blocks = []
        self.annotations = []
        self._open_annotations = {}

    def open_tag(self, tag: HtmlElement) -> None:
        """Register that a tag is opened.

        Args:
            tag: the tag to open.
        """
        if tag.annotation:
            self._open_annotations[tag] = self.current_block.idx

        if tag.display == Display.block:
            self.open_block(tag)

    def open_block(self, tag: HtmlElement) -> None:
        """Open an HTML block element."""
        # write missing bullets, if no content has been written
        if not self.flush_inline() and tag.list_bullet:
            self.write_unconsumed_bullet()
        self.current_block.prefix.register_prefix(tag.padding_inline, tag.list_bullet)

        # write the block margin
        required_margin = max(tag.previous_margin_after, tag.margin_before)
        if required_margin > self.margin:
            required_newlines = required_margin - self.margin
            self.current_block.idx += required_newlines
            self.blocks.append("\n" * (required_newlines - 1))
            self.margin = required_margin

    def write_unconsumed_bullet(self) -> None:
        """Write unconsumed bullets to the blocks list."""
        bullet = self.current_block.prefix.unconsumed_bullet
        if bullet:
            self.blocks.append(bullet)
            self.current_block.idx += len(bullet)
            self.current_block = self.current_block.new_block()
            self.margin = 0

    def write(self, tag: HtmlElement, text: str, whitespace: WhiteSpace = None) -> None:
        """Write the given text to the current block."""
        self.current_block.merge(text, whitespace or tag.whitespace)

    def close_tag(self, tag: HtmlElement) -> None:
        """Register that the given tag tag is closed.

        Args:
            tag: the tag to close.
        """
        if tag.display == Display.block:
            # write missing bullets, if no content has been written so far.
            if not self.flush_inline() and tag.list_bullet:
                self.write_unconsumed_bullet()
            self.current_block.prefix.remove_last_prefix()
            self.close_block(tag)

        if tag in self._open_annotations:
            start_idx = self._open_annotations.pop(tag)
            # do not record annotations with no content
            if start_idx == self.current_block.idx:
                return

            for annotation in tag.annotation:
                self.annotations.append(
                    Annotation(start_idx, self.current_block.idx, annotation)
                )

    def close_block(self, tag: HtmlElement) -> None:
        """Close the given HtmlElement by writing its bottom margin.

        Args:
            tag: the HTML Block element to close
        """
        if tag.margin_after > self.margin:
            required_newlines = tag.margin_after - self.margin
            self.current_block.idx += required_newlines
            self.blocks.append("\n" * (required_newlines - 1))
            self.margin = tag.margin_after

    def write_newline(self) -> None:
        if not self.flush_inline():
            self.blocks.append("")
            self.current_block = self.current_block.new_block()

    def get_text(self) -> str:
        """Provide a text representation of the Canvas."""
        self.flush_inline()
        return "\n".join(self.blocks)

    def flush_inline(self) -> bool:
        """Attempt to flush the content in self.current_block into a new block.

        Notes:
            - If self.current_block does not contain any content (or only
              whitespaces) no changes are made.
            - Otherwise the content of current_block is added to blocks and a
              new current_block is initialized.

        Returns:
            True if the attempt was successful, False otherwise.
        """
        if not self.current_block.is_empty():
            self.blocks.append(self.current_block.content)
            self.current_block = self.current_block.new_block()
            self.margin = 0
            return True

        return False

    @property
    def left_margin(self) -> int:
        """Return the length of the current line's left margin."""
        return self.current_block.prefix.current_padding

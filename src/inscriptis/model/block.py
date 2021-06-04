"""
Representation of a text block within the HTML canvas.
"""
from collections import namedtuple
from inscriptis.html_properties import WhiteSpace

Span = namedtuple('Span', 'start end')


class Block:
    """
    The current block of the text page.

    Args
        idx: the current block's start index.
        prefix: prefix used within the current block.
    """

    __slots__ = ('idx', 'prefix', '_content', 'collapsable_whitespace')

    def __init__(self, idx, prefix):
        self.idx = idx
        self.prefix = prefix
        self._content = ''
        self.collapsable_whitespace = True

    def merge(self, text: str, whitespace: WhiteSpace) -> Span:
        """
        Merges the given text with the current block.

        Args:
            text: the text to merge.
            whitespace: whitespace handling.
        """
        return self.merge_pre_text(text) if whitespace == WhiteSpace.pre \
            else self.merge_normal_text(text)

    def merge_normal_text(self, text: str) -> Span:
        """
        Merges the given text with the current block.

        Args:
            text: the text to merge
        """
        start = self.idx
        normalized_text = []

        for ch in text:
            if not ch.isspace():
                normalized_text.append(ch)
                self.collapsable_whitespace = False
            elif not self.collapsable_whitespace:
                normalized_text.append(' ')
                self.collapsable_whitespace = True

        if normalized_text:
            text = ''.join((next(self.prefix), *normalized_text)) if not \
                self._content else ''.join(normalized_text)
            self._content += text
            self.idx += len(text)

        return Span(start, self.idx)

    def merge_pre_text(self, text: str) -> Span:
        """
        Merges the given text with the current block.

        Args:
            text: the text to merge
        """
        start = self.idx
        text = ''.join((next(self.prefix),
                        text.replace('\n', '\n' + next(self.prefix))))
        self._content += text
        self.idx += len(text)
        self.collapsable_whitespace = False
        return Span(start, self.idx)

    def is_empty(self):
        return len(self.content) == 0

    @property
    def content(self):
        if not self.collapsable_whitespace:
            return self._content

        while self._content.endswith(' '):
            self._content = self._content[:-1]
            self.idx -= 1
        return self._content

    def new_block(self) -> 'Block':
        """
        Returns:
            A new block that follows the current one.
        """
        self.prefix.consumed = False
        return Block(idx=self.idx + 1, prefix=self.prefix)

"""Manage the horizontal prefix (left-indentation, bullets) of canvas lines."""

from contextlib import suppress


class Prefix:
    """Class Prefix manages paddings and bullets that prefix an HTML block.

    Attributes:
        current_padding: the number of characters used for the current
                         left-indentation.
        paddings: the list of paddings for the current and all previous tags.
        bullets: the list of bullets in the current and all previous tags.
        last_used_bullet: the last bullet that has been used.
        consumed: whether the current bullet has already been consumed.
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
        """Register the given prefix.

        Args:
            padding_inline: the number of characters used for padding_inline
            bullet: an optional bullet.
        """
        self.current_padding += padding_inline
        self.paddings.append(padding_inline)
        if bullet:
            self.bullets.append(bullet)
        self.consumed = False

    def remove_last_prefix(self):
        """Remove the last prefix from the list."""
        with suppress(IndexError):
            self.current_padding -= self.paddings.pop()
            del self.bullets[-1]
        self.consumed = False

    @property
    def first(self):
        """Return the prefix used at the beginning of a tag.

        Note::
            A new block needs to be prefixed by the current padding and bullet.
            Once this has happened (i.e., :attr:`consumed` is set to `True`) no
            further prefixes should be used for a line.
        """
        if self.consumed:
            return ''

        self.consumed = True
        self.last_used_bullet = self.bullets.pop(0) if self.bullets else ''
        return ' ' * (self.current_padding - len(self.last_used_bullet)) \
               + self.last_used_bullet

    @property
    def previous(self):
        """Return bullets that have not yet been serialized.

        Note::
            This function yields the previous element's bullets, if they have
            not been consumed yet.
        """
        if self.consumed or not self.bullets:
            return ''

        self.last_used_bullet = self.bullets.pop(0)
        padding = self.current_padding - self.paddings[-1]
        return ' ' * (padding - len(self.last_used_bullet)) \
               + self.last_used_bullet

    @property
    def rest(self):
        """Return the prefix used for new lines within a block.

        This prefix is used for pre-text that contains newlines. The lines
        need to be prefixed with the right padding to preserver the
        indentation.
        """
        return ' ' * self.current_padding

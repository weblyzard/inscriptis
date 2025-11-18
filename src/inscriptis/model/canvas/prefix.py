"""Manage the horizontal prefix (left-indentation, bullets) of canvas lines."""

from contextlib import suppress


class Prefix:
    """Class Prefix manages paddings and bullets that prefix an HTML block.

    Attributes:
        current_padding: the number of characters used for the current
                         left-indentation.
        paddings: the list of paddings for the current and all previous tags.
        bullets: the list of bullets in the current and all previous tags.
        consumed: whether the current bullet has already been consumed.

    """

    __slots__ = ("bullets", "consumed", "current_padding", "paddings")

    def __init__(self) -> None:
        self.current_padding = 0
        self.paddings: list[int] = []
        self.bullets: list[str] = []
        self.consumed = False

    def register_prefix(self, padding_inline: int, bullet: str) -> None:
        """Register the given prefix.

        Args:
            padding_inline: the number of characters used for padding_inline
            bullet: an optional bullet.

        """
        self.current_padding += padding_inline
        self.paddings.append(padding_inline)
        self.bullets.append(bullet if bullet else "")

    def remove_last_prefix(self) -> None:
        """Remove the last prefix from the list."""
        with suppress(IndexError):
            self.current_padding -= self.paddings.pop()
            del self.bullets[-1]

    def pop_next_bullet(self) -> str:
        """Pop the next bullet to use, if any bullet is available."""
        next_bullet_idx = next((-idx for idx, val in enumerate(reversed(self.bullets)) if val), 1) - 1

        if not next_bullet_idx:
            return ""

        bullet = self.bullets[next_bullet_idx]
        self.bullets[next_bullet_idx] = ""
        return bullet

    @property
    def first(self) -> str:
        """Return the prefix used at the beginning of a tag.

        Note::
            A new block needs to be prefixed by the current padding and bullet.
            Once this has happened (i.e., :attr:`consumed` is set to `True`) no
            further prefixes should be used for a line.
        """
        if self.consumed:
            return ""

        self.consumed = True
        bullet = self.pop_next_bullet()
        return " " * (self.current_padding - len(bullet)) + bullet

    @property
    def unconsumed_bullet(self) -> str:
        """Yield any yet unconsumed bullet.

        Note::
            This function yields the previous element's bullets, if they have
            not been consumed yet.
        """
        if self.consumed:
            return ""

        bullet = self.pop_next_bullet()
        if not bullet:
            return ""

        padding = self.current_padding - self.paddings[-1]
        return " " * (padding - len(bullet)) + bullet

    @property
    def rest(self) -> str:
        """Return the prefix used for new lines within a block.

        This prefix is used for pre-text that contains newlines. The lines
        need to be prefixed with the right padding to preserver the
        indentation.
        """
        return " " * self.current_padding

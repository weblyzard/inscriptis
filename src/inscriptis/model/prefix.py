#!/usr/bin/env python
# encoding: utf-8

""" Manages the horizontal prefix (left-indentation, bullets) of canvas
lines. """

from contextlib import suppress


class Prefix:
    """Class Prefix manages paddings and bullets that prefix an HTML block.

    Note:
        In Inscriptis an HTML block corresponds to a line in the final output,
        since new blocks (Display.block) trigger line breaks while inline
        content (Display.normal) does not.

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
        """ Registers the given prefix.

        Args:
            padding_inline: the number of characters used for padding_inline
            bullet: an optional bullet.
        """
        self.current_padding += padding_inline
        self.paddings.append(padding_inline)
        if bullet:
            self.bullets.append(bullet)

    def remove_last_prefix(self):
        """ Remotes the last prefix from the list. """
        with suppress(IndexError):
            self.current_padding -= self.paddings.pop()
            del self.bullets[-1]

    def restore(self):
        """ Restores the last_used_bullet, if present so that the iterator
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

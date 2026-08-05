r"""Provide properties used for rendering HTML pages.

Supported attributes::
 1. :class:`Display` properties.
 2. :class:`WhiteSpace` properties.
 3. :class:`HorizontalAlignment` properties.
 4. :class:`VerticalAlignment` properties.
"""

from enum import Enum


class Display(Enum):
    """Specify whether content will be rendered as inline, block or none.

    .. note::
        A display attribute on none indicates, that the content should not be
        rendered at all.
    """

    inline = 1
    block = 2
    none = 3


class WhiteSpace(Enum):
    """Specify the HTML element's whitespace handling.

    Inscriptis supports the following handling strategies outlined in the
    `Cascading Style Sheets <https://www.w3.org/TR/CSS1/>`_ specification.
    """

    normal = 1
    """Collapse multiple whitespaces into a single one."""
    pre = 3
    """Preserve sequences of whitespaces."""


class HorizontalAlignment(Enum):
    """Specify the content's horizontal alignment."""

    left = "<"
    """Left alignment of the block's content."""
    right = ">"
    """Right alignment of the block's content."""
    center = "^"
    """Center the block's content."""

    def format(self, text: str, width: int) -> str:
        """Format the given text to the specified width using the alignment.

        Args:
            text: The text to format.
            width: The width to format the text to.

        Returns:
            The formatted text.

        """
        match self:
            case HorizontalAlignment.left:
                return text.ljust(width)
            case HorizontalAlignment.right:
                return text.rjust(width)
            case HorizontalAlignment.center:
                return text.center(width)


class VerticalAlignment(Enum):
    """Specify the content's vertical alignment."""

    top = 0
    """Align all content at the top."""
    middle = 1
    """Align all content in the middle."""
    bottom = 2
    """Align all content at the bottom."""

"""Provide properties used for rendering HTML pages.

Supported attributes::
 1. :class:`Display` properties.
 2. :class:`WhiteSpace` properties.
 3. :class:`HorizontalAlignment` properties.
 4. :class:`VerticalAlignment` properites.
"""

from enum import Enum


class Display(Enum):
    """Specify whether content will be rendered as inline, block or none.

    Notes:
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

    .. data:: normal

    Sequences of whitespaces will be collapsed into a single one.

    .. data:: pre

    Sequences of whitespaces will preserved.
    """

    normal = 1
    pre = 3


class HorizontalAlignment(Enum):
    """Specify the content's horizontal alignment."""

    left = '<'
    right = '>'
    center = '^'


class VerticalAlignment(Enum):
    """Specify the content's vertical alignment."""

    top = 1
    middle = 2
    bottom = 3

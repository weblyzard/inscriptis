#!/usr/bin/env python
# encoding: utf-8

"""
This module provides the following properties used for the rendering of HTML
pages:

 1. :class:`Display` properties.
 2. :class:`WhiteSpace` properties.
 3. :class:`HorizontalAlignment` properties.
"""

from enum import Enum


class Display(Enum):
    """
    This enum specifies whether content will be rendered as inline, block or
    none (i.e. not rendered).
    """
    inline = 1
    block = 2
    none = 3


class WhiteSpace(Enum):
    """
    This enum specifies the whitespace handling used for an HTML element as
    outlined in the `Cascading Style Sheets <https://www.w3.org/TR/CSS1/>`_
    specification.

    .. data:: normal

    Sequences of whitespaces will be collapsed into a single one.

    .. data:: pre

    Sequences of whitespaces will preserved.
    """
    normal = 1
    pre = 3


class HorizontalAlignment(Enum):
    """
    This enum specifies the horizontal alignment.
    """
    left = '<'
    right = '>'
    center = '^'


class VerticalAlignment(Enum):
    """
    This enum specifies the vertical alignment.
    """
    top = 1
    middle = 2
    bottom = 3

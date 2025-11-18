"""The model used for saving annotations."""

from typing import NamedTuple

from inscriptis.html_properties import HorizontalAlignment


class Annotation(NamedTuple):
    """An Inscriptis annotation which provides metadata on the extracted text.

    The :attr:`start` and :attr:`end` indices indicate the span of the text
    to which the metadata refers, and the attribute :attr:`metadata` contains
    the tuple of tags describing this span.

    Example::

        Annotation(0, 10, ('heading', ))

    The annotation above indicates that the text span between the 1st (index 0)
    and 11th (index 10) character of the extracted text contains a *heading*.
    """

    start: int
    """the annotation's start index within the text output."""
    end: int
    """the annotation's end index within the text output."""
    metadata: str
    """the tag to be attached to the annotation."""


def horizontal_shift(
    annotations: list[Annotation],
    content_width: int,
    line_width: int,
    align: HorizontalAlignment,
    shift: int = 0,
) -> list[Annotation]:
    r"""Shift annotations based on the given line's formatting.

    Adjusts the start and end indices of annotations based on the line's
    formatting and width.

    Args:
        annotations: a list of Annotations.
        content_width: the width of the actual content
        line_width: the width of the line in which the content is placed.
        align: the horizontal alignment (left, right, center) to assume for
               the adjustment
        shift: an optional additional shift

    Returns:
        A list of :class:`Annotation`\s with the adjusted start and end
        positions.

    """
    if align == HorizontalAlignment.left:
        h_align = shift
    elif align == HorizontalAlignment.right:
        h_align = shift + line_width - content_width
    else:
        h_align = shift + (line_width - content_width) // 2

    return [Annotation(a.start + h_align, a.end + h_align, a.metadata) for a in annotations]

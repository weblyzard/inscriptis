"""The model used for saving annotations."""

from collections import namedtuple
from typing import List

from inscriptis.html_properties import HorizontalAlignment


Annotation = namedtuple('Annotation', 'start end metadata')


def horizontal_shift(annotations: List[Annotation], content_width: int,
                     line_width: int, align: HorizontalAlignment,
                     shift: int = 0) -> List[Annotation]:
    """Adjusts annotation positions according to the given line's formatting
    and width.

    Args:
        annotations: a list of Annotations.
        content_width: the width of the actual content
        line_width: the width of the line in which the content is placed.
        align: the horizontal alignment (left, right, center) to assume for
               the adjustment
        shift: an optional additional shift

    Returns:
        A list of Annotations with the adjusted start and end positions.
    """
    if align == HorizontalAlignment.left:
        h_align = shift
    elif align == HorizontalAlignment.right:
        h_align = shift + line_width - content_width
    else:
        h_align = shift + (line_width - content_width) // 2

    return [Annotation(a.start + h_align, a.end + h_align, a.metadata)
            for a in annotations]

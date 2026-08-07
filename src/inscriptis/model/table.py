#!/usr/bin/env python3
"""Classes used for representing Tables, TableRows and TableCells."""

from __future__ import annotations

from functools import cached_property
from itertools import chain
from typing import TYPE_CHECKING

from inscriptis.annotation import Annotation, horizontal_shift
from inscriptis.model.canvas import Canvas

if TYPE_CHECKING:
    from collections.abc import Sequence

    from inscriptis.html_properties import HorizontalAlignment, VerticalAlignment


class FrozenError(TypeError):
    """Raised when trying to modify a frozen object."""


class BlocksNotNormalizedError(RuntimeError):
    """Raised when an operation requires normalized blocks."""


class TableCell(Canvas):
    """A table cell containing normalized, immutable content.

    A cell has two distinct phases. During construction, its content blocks are
    mutable and may contain multiple lines. Calling `normalize_blocks`
    converts the content into one-line blocks and freezes the cell's content.
    After normalization, the cell's dimensions and alignment may still be
    changed, but its content blocks cannot be modified.

    The cell distinguishes between its content dimensions and its requested
    dimensions. The actual cell width and height are at least as large as the
    content dimensions, while horizontal and vertical alignment determine how
    the content is positioned within any additional space.

    Attributes:
        __dict__: Used by :func:`cached_property` to store cached values.
        _content_blocks: The cell's content blocks. This is a mutable list
            before normalization and an immutable tuple after normalization.
        _width: The requested minimum width of the cell.
        _height: The requested minimum height of the cell.
        _align: The cell's horizontal alignment.
        _valign: The cell's vertical alignment.

    """

    __slots__ = (
        "__dict__",
        "_align",
        "_content_blocks",
        "_height",
        "_valign",
        "_width",
        "annotation_counter",
        "annotations",
        "block_annotations",
        "current_block",
        "margin",
    )

    def __init__(self, align: HorizontalAlignment, valign: VerticalAlignment):
        """Initialize a table cell.

        Args:
            align: The horizontal alignment of the cell's content.
            valign: The vertical alignment of the cell's content.

        """
        super().__init__()
        self._align = align
        self._valign = valign

        # table content (might be smaller than the requested table width and height)
        self._content_blocks: Sequence[str] = []

        # table width and height (might be larger than the content's actual width and height)
        self._height: int = 0
        self._width: int = 0

    def normalize_blocks(self) -> int:
        """Normalize and freeze the cell's content blocks.

        Multi-line blocks are split into individual lines. If the cell has no
        content, a single empty block is created. After normalization, the
        content blocks are immutable and cannot be replaced through ``blocks``.

        Returns:
            The number of normalized content blocks.

        """
        self.flush_inline()
        self._content_blocks = tuple(chain.from_iterable(line.split("\n") for line in self._content_blocks))
        if not self._content_blocks:
            self._content_blocks = ("",)

        return len(self._content_blocks)

    @cached_property
    def _content_width(self) -> int:
        """Return the width of the normalized content.

        Returns:
            The length of the longest content block.

        Raises:
            BlocksNotNormalizedError: If the content has not been normalized.

        """
        if not isinstance(self._content_blocks, tuple):
            msg = "Cannot reliably compute content width before blocks have been normalized."
            raise BlocksNotNormalizedError(msg)
        return max(len(line) for line in self._content_blocks)

    @property
    def blocks(self) -> Sequence[str]:
        """Return the cell's blocks.

        Returns the normalized content blocks when no padding is required;
        otherwise returns the rendered blocks including horizontal and vertical
        padding.

        Returns:
            The cell's content or rendered blocks.

        """
        if self._width > 0 or self._height > len(self._content_blocks):
            return self._rendered_blocks
        return self._content_blocks

    @blocks.setter
    def blocks(self, blocks: list[str]):
        """Set the cell's content blocks.

        Args:
            blocks: The new content blocks.

        Raises:
            FrozenError: If the cell has already been normalized.

        """
        if hasattr(self, "_content_blocks") and isinstance(self._content_blocks, tuple):
            msg = "Cannot modify blocks after they have been normalized."
            raise FrozenError(msg)

        self._content_blocks = blocks

    @cached_property
    def _rendered_blocks(self):
        """Return the content blocks with alignment and padding applied."""
        empty_line = " " * self.width
        return tuple(
            chain(
                (empty_line,) * self._top_padding,
                (self.align.format(line, self.width) for line in self._content_blocks),
                (empty_line,) * (self._height - len(self._content_blocks) - self._top_padding),
            )
        )

    @property
    def align(self) -> HorizontalAlignment:
        return self._align

    @align.setter
    def align(self, align: HorizontalAlignment):
        self._align = align
        self._invalidate_formatting()

    @property
    def valign(self) -> VerticalAlignment:
        return self._valign

    @valign.setter
    def valign(self, valign: VerticalAlignment):
        self._valign = valign
        self._invalidate_formatting()

    @property
    def width(self) -> int:
        """Return the cell's actual width.

        Returns:
            The greater of the content width and the requested minimum width.

        """
        return max(self._content_width, self._width)

    @width.setter
    def width(self, width: int):
        """Set the cell's minimum width.

        Args:
            width: The minimum width of the cell.

        Raises:
            ValueError: If `width` is smaller than the content width.

        """
        if width < self._content_width:
            msg = (
                f"Cannot set cell width to {width} as it is smaller than the content's width of {self._content_width}."
            )
            raise ValueError(msg)
        if width != self._width:
            self._width = width
            self._invalidate_formatting()

    @property
    def height(self) -> int:
        """Return the cell's actual height.

        Returns:
            The greater of the content height and the requested minimum height.

        """
        return max(len(self._content_blocks), self._height)

    @height.setter
    def height(self, height: int):
        """Set the cell's minimum height.

        Args:
            height: The minimum height of the cell.

        Raises:
            ValueError: If `height` is smaller than the content height.

        """
        if height < len(self._content_blocks):
            msg = (
                f"Cannot set cell height to {height} as it is smaller than the content's height "
                f"of {len(self._content_blocks)}."
            )
            raise ValueError(msg)
        if height != self._height:
            self._height = height
            self._invalidate_formatting()

    @property
    def _top_padding(self) -> int:
        """Return the number of blank lines above the cell's content."""
        return (self.height - len(self._content_blocks)) * self.valign.value // 2

    @property
    def _line_width(self) -> tuple[int, ...]:
        """Return the line widths of the cell's content blocks, including vertical padding.

        Note:
            The returned list is `height`-long, with zero-length entries
            filling the top and bottom padding slots, while the remaining
            entries hold the original line widths.

        Returns:
            A list of the original line widths per line.

        """
        return tuple(
            chain(
                (0,) * self._top_padding,
                (len(line) for line in self._content_blocks),
                (0,) * (len(self.blocks) - len(self._content_blocks) - self._top_padding),
            )
        )

    def _invalidate_formatting(self) -> None:
        """Invalidate the cached formatting of the cell."""
        self.__dict__.pop("_rendered_blocks", None)

    def get_annotations(self, idx: int, row_width: int) -> list[Annotation]:
        """Return annotations positioned within the rendered table cell.

        Annotation positions are translated from the cell's unpadded content
        coordinates to their positions in the rendered table, accounting for
        horizontal alignment, vertical padding, and the width of the containing
        table row.

        Args:
            idx: The starting index of the table row in the output.
            row_width: The width of the containing table row.

        Returns:
            The cell's annotations with positions adjusted for the rendered
            table layout.

        """
        self.current_block.idx = idx
        if not self.annotations:
            return []

        # the easy case - the cell has only one line :)
        if self.height == 1:
            content_width = self._line_width[0]
            return horizontal_shift(self.annotations, content_width, self.width, self.align, idx)

        # the more challenging one - multiple cell lines
        #
        # `self._line_width` is `height`-long after vertical padding was
        # applied: zero-length entries fill the top (`self.vertical_padding`)
        # and bottom (for VerticalAlignment.middle) padding slots, while the
        # remaining `len(self._content_blocks)` entries hold the original line
        # widths. Annotation `start` positions reference the *pre-padding*
        # joined content (one newline between lines), so we must scan only
        # the content widths to find which content line an annotation falls
        # on, then offset the destination by the top padding to land on the
        # correct output line.
        line_widths = self._line_width
        top_pad = self._top_padding
        content_widths = line_widths[top_pad : top_pad + len(self._content_blocks)]
        annotation_lines = [[] for _ in self.blocks]

        line_no = 0
        line_end = content_widths[0]

        # Annotations are ordered by start position, allowing us to advance
        # through the content lines only once.
        for annotation in self.annotations:
            while annotation.start > line_end:
                line_no += 1
                line_end += content_widths[line_no] + 1

            annotation_lines[line_no + top_pad].append(annotation)

        # Translate each annotation from content coordinates to rendered
        # table coordinates.
        result = []
        idx += top_pad

        for line_annotations, line_width in zip(
            annotation_lines,
            line_widths,
            strict=False,
        ):
            result.extend(
                horizontal_shift(
                    line_annotations,
                    line_width,
                    self.width,
                    self.align,
                    idx,
                )
            )
            idx += row_width - line_width

        return result


class TableRow:
    """A single row within a table.

    Attributes:
        columns: the table row's columns.
        cell_separator: string used for separating columns from each other.

    """

    __slots__ = ("cell_separator", "columns")

    def __init__(self, cell_separator: str):
        self.columns: list[TableCell] = []
        self.cell_separator = cell_separator

    def __len__(self):
        return len(self.columns)

    def get_text(self) -> str:
        """Return a text representation of the TableRow."""
        row_lines = [
            self.cell_separator.join(line) for line in zip(*[column.blocks for column in self.columns], strict=False)
        ]
        return "\n".join(row_lines)

    @property
    def width(self) -> int:
        """Compute and return the width of the current row."""
        if not self.columns:
            return 0

        return sum(cell.width for cell in self.columns) + len(self.cell_separator) * (len(self.columns) - 1)


class Table:
    """An HTML table.

    Attributes:
        rows: the table's rows.
        left_margin_len: length of the left margin before the table.
        cell_separator: string used for separating cells from each other.

    """

    __slots__ = ("cell_separator", "left_margin_len", "rows")

    def __init__(self, left_margin_len: int, cell_separator: str):
        self.rows = []
        self.left_margin_len = left_margin_len
        self.cell_separator = cell_separator

    def add_row(self):
        """Add an empty :class:`TableRow` to the table."""
        self.rows.append(TableRow(self.cell_separator))

    def add_cell(self, table_cell: TableCell):
        """Add  a new :class:`TableCell` to the table's last row.

        .. note::
            If no row exists yet, a new row is created.
        """
        if not self.rows:
            self.add_row()
        self.rows[-1].columns.append(table_cell)

    def _set_row_height(self):
        """Set the cell height for all :class:`TableCell`s in the table."""
        for row in self.rows:
            max_row_height = max(cell.normalize_blocks() for cell in row.columns) if row.columns else 0
            for cell in row.columns:
                cell.height = max_row_height

    def _set_column_width(self):
        """Set the column width for all :class:`TableCell`s in the table."""
        # determine maximum number of columns
        max_columns = max(len(row.columns) for row in self.rows)

        for cur_column_idx in range(max_columns):
            # determine the required column width for the current column
            max_column_width = max(row.columns[cur_column_idx].width for row in self.rows if len(row) > cur_column_idx)

            # set column width for all TableCells in the current column
            for row in self.rows:
                if len(row) > cur_column_idx:
                    row.columns[cur_column_idx].width = max_column_width

    def get_text(self) -> str:
        """Return and render the text of the given table."""
        if not self.rows:
            return "\n"

        self._set_row_height()
        self._set_column_width()
        return "\n".join(row.get_text() for row in self.rows) + "\n"

    def get_annotations(self, idx: int, left_margin_len: int) -> list[Annotation]:
        r"""Return all annotations in the given table.

        Args:
            idx: the table's start index.
            left_margin_len: len of the left margin (required for adapting
                             the position of annotations).

        Returns:
            A list of all :class:`~inscriptis.annotation.Annotation`\s present
            in the table.

        """
        if not self.rows:
            return []

        annotations = []
        idx += left_margin_len
        for row in self.rows:
            if not row.columns:
                continue

            row_width = row.width + left_margin_len
            row_height = row.columns[0].height
            cell_idx = idx
            for cell in row.columns:
                annotations += cell.get_annotations(cell_idx, row_width)
                cell_idx += cell.width + len(row.cell_separator)

            idx += (row_width + 1) * row_height  # linebreak

        return annotations

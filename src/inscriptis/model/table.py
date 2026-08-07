#!/usr/bin/env python3
"""Classes used for representing Tables, TableRows and TableCells."""

from __future__ import annotations

from typing import Sequence, overload

from itertools import accumulate, chain

from inscriptis.annotation import Annotation, horizontal_shift
from inscriptis.html_properties import HorizontalAlignment, VerticalAlignment
from inscriptis.model.canvas import Canvas

INDEX_ERROR_MSG = "list index out of range"


class FormattedBlockView(Sequence[str]):
    """A view of a list of content blocks that applies horizontal and vertical formatting."""

    __slots__ = ("_cell", "height")

    def __init__(self, cell: TableCell, height: int = 0):
        self._cell: TableCell = cell
        self.height: int = height

    def __len__(self) -> int:
        return max(self.height, len(self._cell._content_blocks))

    @overload
    def __getitem__(self, idx: int) -> str: ...

    @overload
    def __getitem__(self, idx: slice) -> list[str]: ...

    def __getitem__(self, idx: int | slice) -> str | list[str]:
        if isinstance(idx, slice):
            start, stop, step = idx.indices(self._cell.height)
            if step != 1:
                return [self[i] for i in range(start, stop, step)]
            return [self[i] for i in range(start, stop)]

        if idx < 0 or idx >= len(self):
            raise IndexError(INDEX_ERROR_MSG)

        content_idx = idx - self._cell._vertical_padding
        if content_idx < 0 or content_idx >= len(self._cell._content_blocks):
            return " " * self._cell._width

        return self._cell.align.format(self._cell._content_blocks[content_idx], self._cell._width)


class TableCell(Canvas):
    """A table cell.

    Attributes:
        line_width: the original line widths per line (required to adjust
                    annotations after a reformatting)
        vertical_padding: vertical padding that has been introduced due to
                          vertical formatting rules.

    """

    __slots__ = (
        "align",
        "annotation_counter",
        "annotations",
        "block_annotations",
        "current_block",
        "margin",
        "valign",
        "_content_blocks",
        "_formatted_blocks",
        "_width",
        "_vertical_padding",
    )

    def __init__(self, align: HorizontalAlignment, valign: VerticalAlignment):
        super().__init__()
        self.align = align
        self.valign = valign
        self._width: int = 0
        self._vertical_padding = 0
        self._content_blocks: list[str] = []
        self._formatted_blocks: FormattedBlockView | None = None

    def normalize_blocks(self) -> int:
        """Split multi-line blocks into multiple one-line blocks.

        Returns:
            The height of the normalized cell.

        """
        self.flush_inline()
        self._content_blocks = list(chain(*(line.split("\n") for line in self._content_blocks)))
        if not self._content_blocks:
            self._content_blocks = [""]
        return len(self._content_blocks)

    @property
    def blocks(self) -> Sequence[str]:
        """Return the cell's blocks.

        Returns:
            The cell's blocks.

        """
        if self._formatted_blocks:
            return list(self._formatted_blocks)  # remove for optimization
        return self._content_blocks

    @blocks.setter
    def blocks(self, blocks: list[str]):
        """Set the cell's blocks.

        Args:
            blocks: The cell's new blocks.

        """
        self._content_blocks = blocks

    @property
    def width(self) -> int:
        """Compute the table cell's width.

        Returns:
            The cell's current width.

        """
        if self._width > 0:
            return self._width
        return max(map(len, self._content_blocks), default=0)

    @width.setter
    def width(self, width):
        """Set the table's width and applies the cell's horizontal formatting.

        Args:
            width: The cell's expected width.

        """
        # record new width and start reformatting
        self._width = width
        if not self._formatted_blocks:
            self._formatted_blocks = FormattedBlockView(self)

    @property
    def height(self) -> int:
        """Compute the table cell's height.

        Returns:
            The cell's current height.

        """
        return max(0, len(self.blocks))

    @height.setter
    def height(self, height: int):
        """Set the cell's height to the given value.

        Notes:
            Depending on the height and the cell's vertical formatting this
            might require the introduction of empty lines.

        """
        if height <= len(self._content_blocks):
            return

        if not self._formatted_blocks:
            self._formatted_blocks = FormattedBlockView(self, height=height)
        else:
            self._formatted_blocks.height = height

        self._vertical_padding = (height - len(self._content_blocks)) * self.valign.value // 2

    @property
    def line_width(self) -> list[int]:
        """Return the original line widths per line.

        Returns:
            A list of the original line widths per line.

        """
        return [len(line) for line in self._content_blocks]

    def get_annotations(self, idx: int, row_width: int) -> list[Annotation]:
        """Return a list of all annotations within the TableCell.

        Returns:
            A list of annotations that have been adjusted to the cell's
            position.

        """
        self.current_block.idx = idx
        if not self.annotations:
            return []

        # the easy case - the cell has only one line :)
        if len(self.blocks) == 1:
            content_width = self.line_width[0]
            result = horizontal_shift(self.annotations, content_width, self.width, self.align, idx)
            return result

        # the more challenging one - multiple cell lines
        #
        # `self.line_width` is `height`-long after vertical padding was
        # applied: zero-length entries fill the top (`self.vertical_padding`)
        # and bottom (for VerticalAlignment.middle) padding slots, while the
        # remaining `len(self._content_blocks)` entries hold the original line
        # widths. Annotation `start` positions reference the *pre-padding*
        # joined content (one newline between lines), so we must scan only
        # the content widths to find which content line an annotation falls
        # on, then offset the destination by the top padding to land on the
        # correct output line.
        top_pad = self._vertical_padding
        content_widths = self.line_width[top_pad : top_pad + len(self._content_blocks)]
        line_break_pos = list(accumulate(content_widths))
        annotation_lines = [[] for _ in self.blocks]

        # assign annotations to the corresponding line
        for a in self.annotations:
            for no, line_break in enumerate(line_break_pos):
                if a.start <= (line_break + no):  # consider newline
                    annotation_lines[no + top_pad].append(a)
                    break

        # compute the annotation index based on its line and delta :)
        result = []
        idx += self._vertical_padding  # newlines introduced by the padding
        for line_annotations, line_len in zip(annotation_lines, self.line_width, strict=False):
            result.extend(horizontal_shift(line_annotations, line_len, self.width, self.align, idx))
            idx += row_width - line_len
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

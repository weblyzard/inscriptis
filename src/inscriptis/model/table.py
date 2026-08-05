#!/usr/bin/env python3
"""Classes used for representing Tables, TableRows and TableCells."""

from itertools import accumulate, chain

from inscriptis.annotation import Annotation, horizontal_shift
from inscriptis.html_properties import HorizontalAlignment, VerticalAlignment
from inscriptis.model.canvas import Canvas

class TableCell(Canvas):
    """A table cell.

    Attributes:
        line_width: the original line widths per line (required to adjust
                    annotations after a reformatting)
        vertical_padding: vertical padding that has been introduced due to
                          vertical formatting rules.

    """

    __slots__ = (
        "_content_blocks",
        "_formatted_blocks",
        "_height",
        "_width",
        "align",
        "annotation_counter",
        "annotations",
        "block_annotations",
        "current_block",
        "line_width",
        "margin",
        "valign",
        "vertical_padding",
    )

    def __init__(self, align: HorizontalAlignment, valign: VerticalAlignment):
        super().__init__()
        self.align = align
        self.valign = valign
        self._height: int | None = None
        self._width: int | None = None
        self._formatted_blocks: list[str] | None = None
        self._content_blocks: list[str] = []
        self.line_width: list[int]
        self.vertical_padding = 0

    def normalize_blocks(self) -> int:
        """Split multi-line blocks into multiple one-line blocks.

        Normalizes the cell's blocks by splitting multi-line blocks into multiple one-line blocks.
        This is required for computing the cell's height and width.

        Note:
            Each cell has at least one empty block.

        Returns:
            The height of the normalized cell.

        """
        self.flush_inline()
        self._content_blocks = list(chain(*(line.split("\n") for line in self.blocks))) or [""]
        return len(self._content_blocks)

    @property
    def blocks(self) -> list[str]:
        """Return the content blocks and any padding required to satisfy the cell's vertical formatting.

        Returns:
            The cell's content blocks.

        """
        return self._formatted_blocks or self._content_blocks

    @blocks.setter
    def blocks(self, blocks: list[str]):
        """Set the cell's content blocks.

        Args:
            blocks: The cell's content blocks.

        """
        self._content_blocks = blocks

    @property
    def height(self) -> int:
        """Compute the table cell's height.

        Returns:
            The cell's current height.

        """
        return len(self.blocks)

    @property
    def width(self) -> int:
        """Compute the table cell's width.

        Returns:
            The cell's current width.

        """
        if self._width is not None:
            return self._width
        return max(len(line) for line in chain(*(block.split("\n") for block in self.blocks)))

    @width.setter
    def width(self, width):
        """Set the table's width and applies the cell's horizontal formatting.

        Args:
            width: The cell's expected width.

        """
        # save the original line widths before reformatting
        self.line_width = [len(block) for block in self.blocks]

        # record new width and start reformatting
        self._width = width
        self._reformat_blocks()

    @height.setter
    def height(self, height: int):
        """Adjust the _content_blocks to match the given height."""
        if height <= len(self._content_blocks):
            self._formatted_blocks = None
            self.vertical_padding = 0
            return
        self._height = height
        self._reformat_blocks()

    def _reformat_blocks(self) -> None:
        """Reformat the cell's content blocks to match the given width and height."""
        padding = self._height - len(self._content_blocks) if self._height else 0
        format_spec = f"{{:{self.align.value}{self._width}}}" if self._width else "{}"

        top_padding = padding * self.valign.value // 2
        self.vertical_padding = top_padding
        bottom_padding = padding - top_padding

        print(f"top_padding: {top_padding}, bottom_padding: {bottom_padding}, padding: {padding}")

        empty_line = ["" if self._width is None else " " * self._width]
        self._formatted_blocks = (
            top_padding * empty_line
            + [format_spec.format(b) for b in self._content_blocks]
            + bottom_padding * empty_line
        )

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
            self.line_width[0] = self.width
            return result

        # the more challenging one - multiple cell lines
        #
        # `self.line_width` is `height`-long after vertical padding was
        # applied: zero-length entries fill the top (`self.vertical_padding`)
        # and bottom (for VerticalAlignment.middle) padding slots, while the
        # remaining `self._height` entries hold the original line
        # widths. Annotation `start` positions reference the *pre-padding*
        # joined content (one newline between lines), so we must scan only
        # the content widths to find which content line an annotation falls
        # on, then offset the destination by the top padding to land on the
        # correct output line.
        top_pad = self.vertical_padding
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
        idx += self.vertical_padding  # newlines introduced by the padding
        for line_annotations, line_len in zip(annotation_lines, self.line_width, strict=False):
            result.extend(horizontal_shift(line_annotations, line_len, self.width, self.align, idx))
            idx += row_width - line_len
        self.line_width = [self.width for _ in self.line_width]
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

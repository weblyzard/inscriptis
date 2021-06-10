#!/usr/bin/env python3
# encoding: utf-8
"""
Classes for representing Tables, Rows and TableCells.
"""

from typing import List
from itertools import chain, accumulate

from inscriptis.html_properties import HorizontalAlignment, VerticalAlignment
from inscriptis.annotation import Annotation, horizontal_shift
from inscriptis.model.canvas import Canvas


class TableCell(Canvas):
    __slots__ = ('annotations', 'block_annotations', 'blocks', 'current_block',
                 'margin', 'annotation_counter', 'align', 'valign', '_width',
                 'line_width')

    def __init__(self, align: HorizontalAlignment, valign: VerticalAlignment):
        super().__init__()
        self.align = align
        self.valign = valign
        self._width = None
        self.line_width = None

    def normalize_blocks(self) -> int:
        """
        Normalizes the cell by splitting multi-line blocks into multiple ones
        containing only one line.

        Returns:
            The height of the normalized cell.
        """
        self._flush_inline()
        self.blocks = [block for block in chain(*(line.split('\n')
                                                  for line in self.blocks))]
        return len(self.blocks)

    @property
    def height(self):
        """
        Returns:
            The cell's current height.
        """
        return len(self.blocks)

    @property
    def width(self):
        """
        Returns:
            The cell's current width.
        """
        if self._width:
            return self._width
        if not self.blocks:
            return 0
        return max((len(line) for line in chain(*(block.split('\n')
                                                  for block in self.blocks))))

    @width.setter
    def width(self, width) -> None:
        """
        Sets the table's width and apply's the cell's horizontal formatting.

        Args:
            The cell's expected width.
        """
        # save the original line widths before reformatting
        self.line_width = [len(block) for block in self.blocks]

        # record new width and start reformatting
        self._width = width
        format_spec = '{{:{align}{width}}}'.format(align=self.align.value,
                                                   width=width)
        self.blocks = [format_spec.format(b) for b in self.blocks]

    @height.setter
    def height(self, height) -> None:
        """
        Applies the given height and the cell's vertical formatting to
        the current cell.
        """
        rows = len(self.blocks)
        if rows < height:
            empty_line = [' ' * self.width] if self.width else ['']
            if self.valign == VerticalAlignment.bottom:
                self.blocks = ((height - rows) * empty_line) + self.blocks
            elif self.valign == VerticalAlignment.middle:
                self.blocks = ((height - rows) // 2) * empty_line + \
                              self.blocks + \
                              ((height - rows + 1) // 2 * empty_line)
            else:
                self.blocks = self.blocks + ((height - rows) * empty_line)

    def get_annotations(self, idx, row_width) -> List[Annotation]:
        """
        Returns:
            A list of annotations that have been adjusted to the cell's
            position.
        """
        self.current_block.idx = idx
        if not self.annotations:
            return []

        # the easy case - the cell has only one line :)
        if len(self.blocks) == 1:
            return horizontal_shift(self.annotations, self.line_width[0],
                                    self.width, self.align, idx)

        # the more challenging one - multiple cell lines
        line_break_pos = list(accumulate(self.line_width))
        annotation_lines = [list() for _ in self.blocks]

        # assign annotations to the corresponding line
        for a in self.annotations:
            for no, line_break in enumerate(line_break_pos):
                if a.start <= line_break:
                    annotation_lines[no].append(a)
                    break

        # compute the annotation index based on its line and delta :)
        result = []
        for line_annotations, line_len in zip(annotation_lines,
                                              self.line_width):
            result.extend(horizontal_shift(line_annotations, line_len,
                                           self.width, self.align, idx))
            idx += row_width
        return result


class Row:
    """ A single row within a table """
    __slot__ = ('columns', 'cell_separator')

    def __init__(self, cell_separator: str = '  '):
        self.columns: List[TableCell] = []
        self.cell_separator = cell_separator

    def __len__(self):
        return len(self.columns)

    def get_text(self) -> str:
        """
        Returns:
          A rendered string representation of the given row.
        """
        row_lines = [self.cell_separator.join(line)
                     for line in zip(*[column.blocks
                                       for column in self.columns])]
        return '\n'.join(row_lines)

    @property
    def width(self):
        """Computes and returns the width of the current row"""
        if not self.columns:
            return 0

        return sum((cell.width for cell in self.columns)) + len(
            self.cell_separator) * (len(self.columns) - 1)


class Table:
    """ A HTML table. """

    __slot__ = ('rows', 'td_is_open')

    def __init__(self):
        self.rows = []
        # keep track of whether the last td tag has been closed
        self.td_is_open = False

    def add_row(self) -> None:
        """
        Adds an empty :class:`Row` to the table.
        """
        self.rows.append(Row())

    def add_cell(self, table_cell: TableCell) -> None:
        """
        Adds a new :class:`TableCell` to the table's last row. If no row
        exists yet, a new row is created.
        """
        if not self.rows:
            self.add_row()
        self.rows[-1].columns.append(table_cell)

    def compute_column_width_and_height(self):
        """
        Compute and set the column width and height for all columns in the
        table.
        """
        # skip tables with no row
        if not self.rows:
            return

        # determine row height
        for row in self.rows:
            max_row_height = max((cell.normalize_blocks()
                                  for cell in row.columns)) \
                if row.columns else 1
            for cell in row.columns:
                cell.height = max_row_height

        # determine maximum number of columns
        max_columns = max((len(row.columns) for row in self.rows))

        for column_idx in range(max_columns):
            max_column_width = max((row.columns[column_idx].width
                                    for row in self.rows
                                    if len(row) > column_idx)) if self.rows \
                else 0

            # set column width in all rows
            for row in self.rows:
                if len(row) > column_idx:
                    row.columns[column_idx].width = max_column_width

    def get_text(self):
        """
        Returns:
          A rendered string representation of the given table.
        """
        self.compute_column_width_and_height()
        return '\n'.join((row.get_text() for row in self.rows)) + '\n'

    def get_annotations(self, idx: int) -> List[Annotation]:
        """
        Args:
            idx: the table's start index.

        Returns:
            A list of all annotations present in the table.

        """
        if not self.rows:
            return []

        annotations = []
        for row in self.rows:
            row_width = row.width
            cell_idx = idx
            for cell in row.columns:
                if cell.annotations:
                    print(cell.annotations, "idx:", cell_idx, "width:", row_width)
                annotations += cell.get_annotations(cell_idx, row_width)
                cell_idx += cell.width + len(row.cell_separator)
            idx += row_width + 1   # linebreak

        return annotations

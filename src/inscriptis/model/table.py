#!/usr/bin/env python3
# encoding: utf-8
"""
Classes for representing Tables, Rows and TableCells.
"""

from typing import List
from itertools import chain, zip_longest

from inscriptis.html_properties import HorizontalAlignment, VerticalAlignment
from inscriptis.annotation import Annotation
from inscriptis.model.canvas import Canvas


class TableCell(Canvas):
    __slots__ = ('annotations', 'block_annotations', 'blocks', 'current_block',
                 'margin', 'annotation_counter', 'align', 'valign', '_width')

    def __init__(self, align: HorizontalAlignment, valign: VerticalAlignment):
        super().__init__()
        self.align = align
        self.valign = valign
        self._width = None

    def normalize_blocks(self) -> int:
        """
        Normalizes the cell by splitting multi-line blocks into multiple ones
        containing only one line.

        Returns:
            The height of the normalized cell.
        """
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
        self._width = width
        format_spec = '{{:{align}{width}}}'.format(align=self.align.value,
                                                   width=width)
        self.blocks = [format_spec.format(b) for b in self.blocks]
        # TODO: adjust annotations (!)

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
                       self.blocks + ((height - rows + 1) // 2 * empty_line)
            else:
                self.blocks = self.blocks + ((height - rows) * empty_line)


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

    def get_annotations(self, idx: int) -> List[Annotation]:
        """
        Args:
            idx: the start index of the given row.

        Returns:
            The list of all annotations within the given row.
        """
        return []
        annotations = []
        for no, cell in enumerate(self.columns):
            annotations.extend(cell.canvas.get_shifted_annotations(idx))
            # fix: cells can spawn multiple lines (!)
            for line in cell.get_cell_lines(no):
                idx += len(cell.get_cell_lines()) + len(self.cell_separator)
        return annotations


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
        return '\n'.join((row.get_text() for row in self.rows))

    def get_annotations(self, idx: int) -> List[Annotation]:
        annotations = []
        for row in self.rows:
            annotations.extend(row.get_annotations(idx))
            idx += len(row.get_text())
        return annotations


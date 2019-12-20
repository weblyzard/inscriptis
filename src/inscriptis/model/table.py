#!/usr/bin/env python3
# encoding: utf-8
'''
Classes for representing Tables, Rows and TableCells.
'''

from itertools import chain, zip_longest
from inscriptis.html_properties import HorizontalAlignment


class TableCell():
    ''' A single table cell '''

    __slots__ = ('canvas', 'align', 'width', 'height')

    def __init__(self, canvas, align, width=None, height=None):
        '''
        Args:
          canvas: canvas to which the table cell is written.
          align: the :class:`~inscriptis.html_properties.HorizontalAlignment`
            of the given line.
         width: line width
        '''
        self.canvas = canvas
        self.align = align
        self.width = width
        self.height = height

    def get_format_spec(self):
        '''
        The format specification according to the values of `align` and
        `width`.
        '''
        return '{{:{self.align.value}{self.width}}}'.format(self=self)

    def get_cell_lines(self):
        '''
        Returns:
          list -- A list of all the lines stores within the :class:`TableCell`.
        '''
        format_spec = self.get_format_spec()
        # normalize the canvas
        self.canvas = list(chain(*[line.split('\n') for line in self.canvas]))
        if self.height:
            canvas = self.canvas + ((self.height - len(self.canvas)) * [''])
        else:
            canvas = self.canvas
        return [format_spec.format(line) if self.width else line
                for line in canvas]


class Row():
    ''' A single row within a table '''
    __slot__ = ('columns', )

    def __init__(self):
        self.columns = []

    def get_cell_lines(self, column_idx):
        '''
        Computes the list of lines in the cell specified by the column_idx.

        Args:
          column_idx: The column index of the cell.
        Returns:
          list -- The list of lines in the cell specified by the column_idx or
                  an empty list if the column does not exist.
        '''
        return [] if column_idx >= len(self.columns) \
            else self.columns[column_idx].get_cell_lines()

    def get_text(self):
        '''
        Returns:
          str -- A rendered string representation of the given row.
        '''
        row_lines = ['  '.join(line)
                     for line in zip_longest(*[column.get_cell_lines()
                                               for column in self.columns],
                                             fillvalue=' ')]
        return '\n'.join(row_lines)


class Table():
    ''' A HTML table. '''

    __slot__ = ('rows', 'td_is_open')

    def __init__(self):
        self.rows = []
        # keep track of whether the last td tag has been closed
        self.td_is_open = False

    def add_row(self):
        '''
        Adds an empty :class:`Row` to the table.
        '''
        self.rows.append(Row())

    def add_cell(self, canvas, align=HorizontalAlignment.left):
        '''
        Adds a new :class:`TableCell` to the table's last row. If no row
        exists yet, a new row is created.
        '''
        if not self.rows:
            self.add_row()
        self.rows[-1].columns.append(TableCell(canvas, align))

    def compute_column_width_and_height(self):
        '''
        Compute and set the column width and height for all colls in the table.
        '''
        # skip tables with no row
        if not self.rows:
            return

        # determine row height
        for row in self.rows:
            max_row_height = max((len(cell.get_cell_lines())
                                  for cell in row.columns)) \
                                  if row.columns else 1
            for cell in row.columns:
                cell.height = max_row_height

        # determine maximum number of columns
        max_columns = max([len(row.columns) for row in self.rows])

        for column_idx in range(max_columns):
            # determine max_column_width
            row_cell_lines = [row.get_cell_lines(column_idx)
                              for row in self.rows]
            max_column_width = max((len(line)
                                    for line in chain(*row_cell_lines)))

            # set column width in all rows
            for row in self.rows:
                if len(row.columns) > column_idx:
                    row.columns[column_idx].width = max_column_width

    def get_text(self):
        '''
        Returns:
          A rendered string representation of the given table.
        '''
        self.compute_column_width_and_height()
        return '\n'.join((row.get_text() for row in self.rows))

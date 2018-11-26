#!/usr/bin/env python3
# encoding: utf-8


class TableCell:
    ''' A single table cell '''

    __slots__ = ('canvas', 'align', 'width')

    def __init__(self, canvas, align, width=None):
        '''
        ::param: canvas \
            canvas to which the table cell is written
        ::param: align \
            the line's alignment using string.format's format specification
                 * '<': left
                 * '>': right
                 * '^': center
        ::param width: line width
        '''
        self.canvas = canvas
        self.align = align
        self.width = width

    def get_format_spec(self):
        '''
        The format specification according to the values of `align` and `width`
        '''
        return u"{{:{align}{width}}}".format(align=self.align, width=self.width)

    def get_text(self):
        text = '\n'.join(self.canvas).strip()
        return self.get_format_spec().format(text) if self.width else text


class Table(object):
    ''' A HTML table. '''

    __slot__ = ('rows', 'td_is_open')

    def __init__(self):
        self.rows = []
        # keep track of whether the last td tag has been closed
        self.td_is_open = False

    def add_row(self):
        self.rows.append(Row())

    def add_cell(self, canvas, align='<'):
        if not self.rows:
            self.add_row()
        self.rows[-1].columns.append(TableCell(canvas, align))

    def compute_column_width(self):
        '''
        compute and set the column width for all colls in the table
        '''
        # skip tables with no or only one row
        if len(self.rows) <= 1:
            return

        # determine maximum number of columns
        max_columns = max([len(row.columns) for row in self.rows])

        for column_idx in range(max_columns):
            # determine max_column_width
            max_column_width = max(
                [len(row.get_cell_text(column_idx)) for row in self.rows])

            # set column width in all rows
            for row in self.rows:
                if len(row.columns) > column_idx:
                    row.columns[column_idx].width = max_column_width

    def get_text(self):
        '''
            ::returns:
            a rendered string representation of the given table
        '''
        self.compute_column_width()
        return '\n'.join((row.get_text() for row in self.rows))


class Row(object):
    ''' A single row within a table '''
    __slot__ = ('columns', )

    def __init__(self):
        self.columns = []

    def get_cell_text(self, column_idx):
        '''
            ''returns:
            the text at the column_idx or an empty Line if the column does not exist
        '''
        return '' if column_idx >= len(self.columns) else self.columns[column_idx].get_text()

    def get_text(self):
        '''
            ::returns:
            a rendered string representation of the given row

            ::note
                ... we currently do not allow any newlines in a column
        '''
        return ' '.join((column.get_text().replace('\n', ' ') for column in self.columns))

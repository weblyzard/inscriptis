#!/usr/bin/env python3
# encoding: utf-8

from inscriptis.html_properties import Line

class Table(object):
    ''' A HTML table. '''

    __slot__ = ('rows', 'align')

    def __init__(self):
        self.rows = []

    def add_row(self):
        self.rows.append(Row())

    def add_column(self, align='<'):
        if not self.rows:
            self.add_row()
        self.rows[-1].columns.append(Line(align=align))

    def add_text(self, text):
        ''' adds text to the current column

        ::note
            the component calling add_text _must ensure_ that at least one
            column has been added to the table.

        '''
        self.rows[-1].columns[-1].content += text

    def compute_column_width(self):
        '''
        compute and set the column width for all colls in the table
        '''
        # skip tables with no or only one row
        if len(self.rows) <= 1:
            return

        empty_line = Line()

        # determine maximum number of columns
        max_columns = max([len(row.columns) for row in self.rows])

        for column_idx in range(max_columns):
            # determine max_column_width
            max_column_width = max([len(row.get_cell_text(column_idx).get_text().strip()) for row in self.rows])

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
        return Line() if column_idx >= len(self.columns) else self.columns[column_idx]


    def get_text(self):
        '''
            ::returns:
            a rendered string representation of the given row

            ::note
                ... we currently do not allow any newlines in a column
        '''
        return ' '.join((column.get_text().replace('\n', ' ') for column in self.columns))


#!/usr/bin/env python3
# encoding: utf-8

from inscriptis.html_properties import Line

class Table(object):
    ''' A HTML table. '''

    __slot__ = ('rows', )

    def __init__(self):
        self.rows = []

    def add_row(self):
        self.rows.append(Row())

    def add_column(self):
        if not self.rows:
            self.add_row()
        self.rows[-1].columns.append(Line())

    def add_text(self, text):
        ''' adds text to the current column

        ::note
            the component calling add_text _must ensure_ that at least one
            column has been added to the table.

        '''
        self.rows[-1].columns[-1].content += text

    def get_text(self):
        '''
            ::returns:
            a rendered string representation of the given table
        '''
        return '\n'.join((row.get_text() for row in self.rows))


class Row(object):
    ''' A single row within a table '''
    __slot__ = ('columns', )

    def __init__(self):
        self.columns = []

    def get_text(self):
        '''
            ::returns:
            a rendered string representation of the given row

            ::note
                ... we currently do not allow any newlines in a column
        '''
        return '\t'.join((column.get_text().replace('\n', ' ') for column in self.columns))


#!/usr/bin/env python3
# encoding: utf-8

class Display(object):
    inline = 1
    block = 2
    none = 3

class WhiteSpace(object):
    normal = 1 # sequences of whitespace will collapse into a single one
    pre = 3    # sequences of whitespace will be preserved


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
        self.rows[-1].columns.append("")

    def add_text(self, text):
        ''' adds text to the current column '''
        self.rows[-1].columns[-1] += text

    def __str__(self):
        '''
            ::returns:
            a rendered string representation of the given table
        '''
        return '\n'.join((str(row) for row in self.rows))

class Row(object):
    ''' A single row within a table '''
    __slot__ = ('columns', )

    def __init__(self):
        self.columns = []

    def __str__(self):
        '''
            ::returns:
            a rendered string representation of the given row
        '''
        return '\t'.join(self.columns)


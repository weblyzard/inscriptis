#!/usr/bin/env python
# encoding: utf-8

'''
Elements used for rendering (parts) of the canvas.

 1. the :class:`Line` determines how a single line is rendered.
'''


class Line(object):
    '''
    This class represents a line to render.

    Args:
        margin_before: number of empty lines before the given line.
        margin_after: number of empty lines before the given line.
        prefix: prefix add before the line's content.
        suffix: suffix to add after the line's content.
        list_bullet: a bullet to add before the line.
        padding: horizontal padding
        align: determines the alignment of the line (not used yet)
        width: total width of the line in characters (not used yet)
    '''
    __slots__ = ('margin_before', 'margin_after', 'prefix', 'suffix',
                 'content', 'list_bullet', 'padding', 'align', 'width')

    def __init__(self):
        self.margin_before = 0
        self.margin_after = 0
        self.prefix = ""
        self.suffix = ""
        self.content = ""
        self.list_bullet = ""
        self.padding = 0

    def get_text(self):
        '''
        Returns:
          str -- The text representation of the current line.
        '''
        return ''.join(('\n' * self.margin_before,
                        ' ' * (self.padding - len(self.list_bullet)),
                        self.list_bullet,
                        self.prefix,
                        ' '.join(self.content.split()),
                        self.suffix,
                        '\n' * self.margin_after))

    def __str__(self):
        return "<Line: '{}'>".format(self.get_text())

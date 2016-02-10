#!/usr/bin/env python3
# encoding: utf-8

class Display(object):
    inline = 1
    block = 2
    none = 3

class WhiteSpace(object):
    normal = 1 # sequences of whitespace will collapse into a single one
    pre = 3    # sequences of whitespace will be preserved

class Line(object):
    '''
    Object used to represent a line
    '''
    __slots__ = ('margin_before', 'margin_after', 'prefix', 'suffix',
                 'content', 'list_bullet', 'padding')

    def __init__(self):
        self.margin_before = 0
        self.margin_after = 0
        self.prefix = ""
        self.suffix = ""
        self.content = ""
        self.list_bullet = ""
        self.padding = 0

    def extract_pre_text(self):
        pass

    def get_text(self):
        # print(">>" + self.content + "<< before: " + str(self.margin_before) + ", after: " + str(self.margin_after) + ", padding: ", self.padding, ", list: ", self.list_bullet)
        return ''.join(('\n' * self.margin_before,
                        ' ' * (self.padding - len(self.list_bullet)),
                        self.list_bullet,
                        self.prefix,
                        ' '.join(self.content.split()),
                        self.suffix,
                        '\n' * self.margin_after))
    def __str__(self):
        self.get_text()

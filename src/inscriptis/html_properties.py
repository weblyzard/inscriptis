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

    Format specification:
    =====================
    - align: the line's alignment using string.format's format specification
             * '<': left
             * '>': right
             * '^': center
    - width: line width

    '''
    __slots__ = ('margin_before', 'margin_after', 'prefix', 'suffix',
                 'content', 'list_bullet', 'padding', 'align', 'width')

    def __init__(self, align=None):
        self.margin_before = 0
        self.margin_after = 0
        self.prefix = ""
        self.suffix = ""
        self.content = ""
        self.list_bullet = ""
        self.padding = 0

        # alignment options
        self.align = align
        self.width = None

    def extract_pre_text(self):
        pass

    def get_format_spec(self):
        '''
        The format specification according to the values of `align` and `width`
        '''
        return "{{:{align}{width}}}".format(align=self.align, width=self.width)

    def get_text(self):
        # print(">>" + self.content + "<< before: " + str(self.margin_before) + ", after: " + str(self.margin_after) + ", padding: ", self.padding, ", list: ", self.list_bullet)
        text = ''.join(('\n' * self.margin_before,
                        ' ' * (self.padding - len(self.list_bullet)),
                        self.list_bullet,
                        self.prefix,
                        ' '.join(self.content.split()),
                        self.suffix,
                        '\n' * self.margin_after))

        return self.get_format_spec().format(text) if self.align and self.width else text


#!/usr/bin/env python
# coding:utf-8
'''
Converts HTML to Text

Guiding principles:

 a. break lines only if we encounter a block element
 b. paddings:
'''

__author__ = "Fabian Odoni, Albert Weichselbraun, Samuel Abels"
__copyright__ = "Copyright 2015, HTW Chur"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Fabian Odoni"
__email__ = "fabian.odoni@htwchur.ch"
__status__ = "Prototype"

try: # python 3.x
    from html.parser import HTMLParser
    from urllib.request import urlopen
except ImportError: # python 2.x
    from HTMLParser import HTMLParser
    from urllib import urlopen
    from io import open

from bs4 import BeautifulSoup
from inscriptis.css import CSS, HtmlElement
from inscriptis.html_properties import Display, WhiteSpace

import argparse

class Line(object):
    '''
    Object used to represent a line
    '''

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
        print(">>" + self.content + "<< before: " + str(self.margin_before) + ", after: " + str(self.margin_after) + ", padding: ", self.padding, ", list: ", self.list_bullet)
        return ''.join(['\n' * self.margin_before,
                        ' ' * (self.padding - len(self.list_bullet)),
                        self.list_bullet,
                        self.prefix,
                        ' '.join(self.content.split()),
                        self.suffix,
                        '\n' * self.margin_after])


class Cell:
    data = ''
    colspan = 1
    rowspan = 1


class Parser(HTMLParser):

    ul_counter = ['* ', '+ ', 'o ', '- '] * 10

    def __init__(self):
        HTMLParser.__init__(self)
        # self.current_tag = [HtmlElement()] # a stack containing information on the current tag
        self.current_tag = [HtmlElement()]
        self.current_line = Line()
        self.next_line = Line()
        self.clean_text_lines = []
        self.buffer = ''
        self.indent = 0
        self.rows = []
        self.cells = []
        self.in_table = False
        self.in_td = False
        self.in_heading = False
        self.li_counter = []
        self.li_level = 0

    def get_text(self):
        '''
        ::returns:
           a text representation of the parsed content
        '''
        if self.current_line:
            self.__flush()
            self.current_line = None
        return '\n'.join(self.clean_text_lines)

    def __output(self, text):
        self.buffer += (' ' * self.indent * 2)
        self.buffer += text
        if self.buffer[-2:] != '\n' and len(self.buffer) > 0:
            self.buffer += '\n'

    def __flush(self):
        '''
        Writes the current line to the buffer, provided that there is any
        data to write.

        ::returns:
            True, if a line has been writer, otherwise False
        '''
        print("___>" + ' '.join(self.current_line.content.split()) + "<<<")
        print("PRN>", (self.current_line.content.strip() != ""))

        # only break the line if there is any relevant content
        if not self.current_line.content.strip():
            self.current_line.margin_before = max(self.current_line.margin_before, \
                                                  self.current_tag[-1].margin_before)
            return False
        else:
            self.clean_text_lines.append(self.current_line.get_text())
            self.current_line = self.next_line
            self.next_line = Line()
            return True

    def handle_starttag(self, tag, attrs):
        # use the css to handle tags known to it :)
        cur = CSS.get(tag, HtmlElement())
        self.current_tag.append(cur)
        self.next_line.margin_before = max(self.next_line.margin_before, cur.margin_before)
        self.next_line.padding = self.current_line.padding + cur.padding
        # flush text before display:block elements
        if cur.display == Display.block:
            if not self.__flush():
                self.current_line.margin_before = self.next_line.margin_before
                self.current_line.padding = self.next_line.padding

        if tag == 'table': self.start_table()
        elif tag == 'tr': self.start_tr()
        elif tag == 'th': self.start_th(attrs)
        elif tag == 'td': self.start_td(attrs)
        elif tag == 'ul': self.start_ul()
        elif tag == 'ol': self.start_ol()
        elif tag == 'li': self.start_li(tag)
        elif tag == 'br': self.newline()

    def handle_endtag(self, tag):
        cur = self.current_tag.pop()
        self.next_line.padding = self.current_line.padding - cur.padding
        self.current_line.margin_after = max(self.current_line.margin_after, cur.margin_after)
        # flush text after display:block elements
        if cur.display == Display.block:
            # propagate the new padding to the current line, if nothing has
            # been written
            if not self.__flush():
                self.current_line.padding = self.next_line.padding

        if tag == 'table': self.end_table()
        elif tag == 'tr': self.end_tr()
        elif tag == 'th': self.end_th()
        elif tag == 'td': self.end_td()
        elif tag == 'ul': self.end_ul()
        elif tag == 'ol': self.end_ol()

    def handle_data(self, data):
        # protect pre areas
        if self.current_tag[-1].whitespace == WhiteSpace.pre:
            data = '\0' + data + '\0'

        self.current_line.content += data

    def start_ul(self):
        self.li_level += 1
        self.li_counter.append(Parser.ul_counter[self.li_level-1])

    def end_ul(self):
        self.li_level -= 1
        self.li_counter.pop()

    def start_ol(self):
        self.li_counter.append(1)
        self.li_level += 1

    def end_ol(self):
        self.li_level -= 1
        self.li_counter.pop()

    def start_li(self, tag):
        self.__flush()
        if self.li_level > 0:
            bullet = self.li_counter[-1]
        else:
            bullet = "* "
        if isinstance(bullet, int):
            self.li_counter[-1] += 1
            self.current_line.list_bullet = "{}. ".format(bullet)
        else:
            self.current_line.list_bullet = bullet

    def start_table(self):
        self.in_table = True

    def start_tr(self):
        pass

    def start_th(self, attrs):
        self.in_heading = True
        self.start_td(attrs)

    def start_td(self, attrs):
        self.__flush()
        self.in_td = True
        cell = Cell()
        for key, value in attrs:
            if key == 'rowspan':
                cell.rowspan = int(value)
            elif key == 'colspan':
                cell.colspan = int(value)
        self.cells.append(cell)

    def end_td(self):
        if len(self.cells) > 0:
            self.cells[-1].data += self.buffer
        self.buffer = ''
        self.in_td = False

    def end_th(self):
        self.end_td()

    def end_tr(self):
        if len(self.cells) is 0:
            return
        if self.in_heading:
            self.__output('')
            self.in_heading = False
        else:
            self.__output('')
        self.indent += 1
        line = ('\t' * self.cells[0].colspan) + ' ' + self.cells[0].data.replace('\n', '')
        for cell in self.cells[1:]:
            line += ' ' + ('\t' * cell.colspan) + ' ' + cell.data.replace('\n', '')

        if len(line) <= 80:
            self.__output(line)
        else:
            for cell in self.cells:
                self.__output(('\t' * cell.colspan) + ' ' + cell.data.replace('\n', ''))
        self.cells = []
        self.indent -= 1
        self.__flush()

    def end_table(self):
        self.in_table = False
        self.buffer += '\n'
        self.__flush()

    def newline(self):
        self.buffer += '\n'



def clean_html(input_data):
    """ Cleans up the HTML Code """
    soup = BeautifulSoup(input_data, "lxml")
    for script in soup(["script", "style"]):
        script.extract()

    html = str(soup)
    return html


def get_text_from_html(input_data):
    """ Turns HTML into text """
    parser = Parser()
    input_data = clean_html(input_data)
    parser.feed(input_data)
    result = parser.get_text()

    return result


def get_args():
    """ Parses the arguments if script is run directly via console """
    parser = argparse.ArgumentParser(description='Converts HTML from file or url to a clean text version')
    parser.add_argument('input', help='Html input either from a file or an url')
    parser.add_argument('-o', '--output', type=str, help='Output file (default:stdout).')
    parser.add_argument('-e', '--encoding', type=str, help='Content encoding for files (default:utf-8)', default='utf-8')
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = get_args()

    if args.input.startswith("http://") or args.input.startswith("https://"):
        html_content = urlopen(args.input)
    else:
        with open(args.input, encoding=args.encoding) as f:
            html_content = f.read()

    text = get_text_from_html(html_content)
    if args.output:
        with open(args.output, 'w') as open_file:
            open_file.write(text)
    else:
        print(text)

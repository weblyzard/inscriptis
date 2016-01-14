#!/usr/bin/env python
# coding:utf-8
"""
Converts HTML to Text
"""

__author__ = "Fabian Odoni, Albert Weichselbraun, Samuel Abels"
__copyright__ = "Copyright 2015, HTW Chur"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Fabian Odoni"
__email__ = "fabian.odoni@htwchur.ch"
__status__ = "Prototype"

from html.parser import HTMLParser
from bs4 import BeautifulSoup
import urllib
import argparse


class Cell:
    data = ''
    colspan = 1
    rowspan = 1


class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.wiki = ''
        self.buffer = ''
        self.indent = 0
        self.rows = []
        self.cells = []
        self.in_table = False
        self.in_td = False
        self.in_heading = False
        self.in_ul = False
        self.in_ol = False
        self.ol_nr = False
        self.in_li = False
        self.li_lvl = 0
        self.in_a = False
        self.in_pre = False
        self.last_href = ''
        self.span_path = []
        self.bullet_points = ['', '*', '+', 'o', '-'] * 10

    def __output(self, text):
        self.buffer += (' ' * self.indent * 2)
        self.buffer += text
        if self.buffer[-2:] != '\n' and len(self.buffer) > 0:
            self.buffer += '\n'

    def __flush(self):
        self.wiki += self.buffer
        self.buffer = ''

    def __if_not_then_append(self, ifnot):
        if not self.buffer.endswith(ifnot):
            self.buffer += ifnot

    def handle_starttag(self, tag, attrs):
        if   tag == 'table': self.start_table()
        elif tag == 'tr': self.start_tr()
        elif tag == 'th': self.start_th(attrs)
        elif tag == 'td': self.start_td(attrs)
        elif tag == 'h1': self.start_h1()
        elif tag == 'h2': self.start_h2()
        elif tag == 'h3': self.start_h3()
        elif tag == 'p': self.start_p()
        elif tag == 'ul': self.start_ul()
        elif tag == 'ol': self.start_ol()
        elif tag == 'li': self.start_li(tag)
        elif tag == 'i': self.start_i()
        elif tag == 'b': self.start_b()
        elif tag == 'u': self.start_u()
        elif tag == 'a': self.start_a(attrs)
        elif tag == 'pre': self.start_pre()
        elif tag == 'strike': self.start_strike()
        elif tag == 'span': self.start_span(attrs)
        elif tag == 'br': self.newline()
        elif tag == 'div': self.start_div()

    def handle_endtag(self, tag):
        if   tag == 'table':  self.end_table();
        elif tag == 'tr': self.end_tr()
        elif tag == 'th': self.end_th()
        elif tag == 'td': self.end_td()
        elif tag == 'h1': self.end_h1()
        elif tag == 'h2': self.end_h2()
        elif tag == 'h3': self.end_h3()
        elif tag == 'p': self.end_p()
        elif tag == 'ul': self.end_ul()
        elif tag == 'ol': self.end_ol()
        elif tag == 'li': self.end_li(tag)
        elif tag == 'i': self.end_i()
        elif tag == 'b': self.end_b()
        elif tag == 'u': self.end_u()
        elif tag == 'a': self.end_a()
        elif tag == 'pre': self.end_pre()
        elif tag == 'strike': self.end_strike()
        elif tag == 'span': self.end_span()
        elif tag == 'div': self.start_div()

    def start_h1(self):
        self.__if_not_then_append('\n\n')

    def end_h1(self):
        self.__if_not_then_append('\n\n')

    def start_h2(self):
        self.__if_not_then_append('\n\n')

    def end_h2(self):
        self.__if_not_then_append('\n\n')

    def start_h3(self):
        self.__if_not_then_append('\n\n')

    def end_h3(self):
        self.__if_not_then_append('\n\n')

    def start_p(self):
        self.__if_not_then_append('\n\n')

    def end_p(self):
        self.__if_not_then_append('\n\n')

    def start_ul(self):
        self.in_ul = True

    def end_ul(self):
        self.in_ul = False

    def start_ol(self):
        self.in_ol = True

    def end_ol(self):
        self.ol_nr = False
        self.in_ol = False

    def start_li(self, tag):
        self.li_lvl += 1

        if self.in_ol:
            self.ol_nr += 1
            self.buffer += '\n{}{}. '.format('\t' * self.li_lvl, str(self.ol_nr))

        elif self.in_ul:
            self.buffer += '\n{}{} '.format('\t' * self.li_lvl, self.bullet_points[self.li_lvl])

        else:
            self.buffer += '\n{}{} '.format('\t' * self.li_lvl, self.bullet_points[self.li_lvl])

    def end_li(self, tag):
        self.li_lvl -= 1

    def start_i(self):
        pass

    def end_i(self):
        pass

    def start_b(self):
        pass

    def end_b(self):
        pass

    def start_u(self):
        pass

    def end_u(self):
        pass

    def start_a(self, attrs):
        self.in_a = True
        self.last_href = ''
        for key, value in attrs:
            if key == 'href':
                self.last_href = value

    def end_a(self):
        self.in_a = False

    def start_pre(self):
        self.in_pre = True

    def end_pre(self):
        self.in_pre = False

    def start_strike(self):
        pass

    def end_strike(self):
        pass

    def start_span(self, attrs):
        pass

    def end_span(self):
        pass

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

    def handle_data(self, data):
        if not self.in_pre:
            data = data.replace('\n', '')

        if self.in_a:
            if data == self.last_href:
                return

        if self.li_lvl > 0:
            self.buffer += data
            return

        if self.in_ul or self.in_ol:
            self.__flush()
            return

        if self.in_td:
            self.buffer += data
        elif not self.in_table:
            self.buffer += data
            self.__flush()

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

    def start_div(self):
        self.__if_not_then_append('\n')

    def end_div(self):
        self.__if_not_then_append('\n')


def get_html(url_input):
    """ """
    return urllib.request.urlopen(url_input)


def clean_html(input_data):
    """ """
    soup = BeautifulSoup(input_data, "lxml")
    for script in soup(["script", "style"]):
        script.extract()

    html = str(soup).strip('\t\r\n')

    '''
    bad_tags = ['<i>', '</i>', '<b>', '</b>', '<u>', '</u>']
    for tag in bad_tags:
        html = html.replace(tag, '')
    # '''

    return html


def clean_text(text):
    """ """
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    text = "".join(text)
    text = text.replace('  ', ' ')
    text = text.replace(' \t', '\t')
    text = text.replace('\t ', '\t')

    return text


def get_text(input_data):
    """ """
    parser = Parser()
    parser.feed(input_data)
    result = parser.wiki
    result = clean_text(result)

    return result


def get_text_from_url(url):
    """ """
    html = get_html(url)
    html = clean_html(html.read())
    text = get_text(html)

    return text


def get_args():
    """ """
    parser = argparse.ArgumentParser(description='Converts HTML from file or url to a clean text version')
    parser.add_argument('-u', '--input', help='Html input either from a file or an url')
    parser.add_argument('input', nargs='?', help='Html input either from a file or an url')
    parser.add_argument('-o', '--output', type=str, help='Define file to save output to')
    parser.add_argument('-p', '--printout', action='store_true', help='Print the output on the console')
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = get_args()

    if not args.input:
        url = "http://www.informationscience.ch"
    else:
        url = args.input

    text = get_text_from_url(url)

    if args.output:
        with open(args.output, 'w') as open_file:
            for line in text:
                open_file.write(line)

    if args.printout:
        print(text)

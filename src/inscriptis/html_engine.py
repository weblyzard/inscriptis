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

from lxml.html import fromstring
from inscriptis.css import CSS, HtmlElement
from inscriptis.html_properties import Display, WhiteSpace, Table

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
        return ''.join(['\n' * self.margin_before,
                        ' ' * (self.padding - len(self.list_bullet)),
                        self.list_bullet,
                        self.prefix,
                        ' '.join(self.content.split()),
                        self.suffix,
                        '\n' * self.margin_after])


class Inscriptis(object):

    ul_counter = ('* ', '+ ', 'o ', '- ') * 10

    def __init__(self, html_tree, display_images=True, deduplicate_captions=True):
        '''
        ::param: display_images \
            whether to include image tiles/alt texts
        ::param: deduplicate_captions \
            whether to deduplicate captions such as image titles
            (many newspaper include images and video previews with
             identifical titles).
        '''
        self.cfg_display_images = display_images
        self.cfg_deduplicate_captions = deduplicate_captions

        self.current_tag = [HtmlElement()]
        self.current_line = Line()
        self.next_line = Line()
        self.clean_text_lines = []
        self.buffer = ''
        self.current_table = []
        self.li_counter = []
        self.li_level = 0
        self.invisible = [] # a list of attributes that are considered invisible
        self.last_caption = None

        # crawl the html tree
        self.crawl_tree(html_tree)
        if self.current_line:
            self.__flush()

    def crawl_tree(self, tree):
        if type(tree.tag) is str:
            self.handle_starttag(tree.tag, tree.attrib)
            if tree.text:
                self.handle_data(tree.text)

            for node in tree:
                self.crawl_tree(node)

            self.handle_endtag(tree.tag)

        if tree.tail:
            self.handle_data(tree.tail)

    def get_text(self):
        '''
        ::returns:
           a text representation of the parsed content
        '''
        return '\n'.join(self.clean_text_lines)

    def __flush(self, force=False):
        '''
        Writes the current line to the buffer, provided that there is any
        data to write.

        ::returns:
            True, if a line has been writer, otherwise False
        '''
        # only break the line if there is any relevant content
        if not force and not self.current_line.content.strip():
            self.current_line.margin_before = max(self.current_line.margin_before, \
                                                  self.current_tag[-1].margin_before)
            return False
        else:
            line = self.current_line.get_text()
            if len(self.current_table) > 0:
                self.current_table[-1].add_text(line.replace('\n', ' '))
            else:
                self.clean_text_lines.append(line)

            self.current_line = self.next_line
            self.next_line = Line()
            return True

    def __flush_verbatim(self, text):
        '''
        Writes the current buffer without any modifications.
        '''
        self.clean_text_lines.append(text)

    def handle_starttag(self, tag, attrs):
        # use the css to handle tags known to it :)

        cur = CSS.get(tag, HtmlElement())
        self.current_tag.append(cur)
        if cur.display == Display.none or self.invisible or ('style' in attrs and 'display:none' in attrs['style']):
            self.invisible.append(cur)
            return

        self.next_line.padding = self.current_line.padding + cur.padding
        # flush text before display:block elements
        if cur.display == Display.block:
            if not self.__flush():
                self.current_line.margin_before = max(self.current_line.margin_before, cur.margin_before)
                self.current_line.padding = self.next_line.padding
            else:
                self.current_line.margin_after = cur.margin_before

        if tag == 'table': self.start_table()
        elif tag == 'tr': self.start_tr()
        elif tag == 'td': self.start_td()
        elif tag == 'th': self.start_td()
        elif tag == 'ul': self.start_ul()
        elif tag == 'ol': self.start_ol()
        elif tag == 'li': self.start_li()
        elif tag == 'br': self.newline()
        elif tag == 'img' :self.start_img(attrs)

    def handle_endtag(self, tag):
        cur = self.current_tag.pop()
        if self.invisible:
            self.invisible.pop()
            return

        self.next_line.padding = self.current_line.padding - cur.padding
        self.current_line.margin_after = max(self.current_line.margin_after, cur.margin_after)
        # flush text after display:block elements
        if cur.display == Display.block:
            # propagate the new padding to the current line, if nothing has
            # been written
            if not self.__flush():
                self.current_line.padding = self.next_line.padding

        if tag == 'table': self.end_table()
        elif tag == 'ul': self.end_ul()
        elif tag == 'ol': self.end_ol()
        elif tag == 'td': self.end_td()
        elif tag == 'th': self.end_td()

    def handle_data(self, data):
        if self.invisible:
            return

        # protect pre areas
        if self.current_tag[-1].whitespace == WhiteSpace.pre:
            data = '\0' + data + '\0'

        self.current_line.content += data

    def start_ul(self):
        self.li_level += 1
        self.li_counter.append(Inscriptis.ul_counter[self.li_level-1])

    def start_img(self, attrs):
        if self.cfg_display_images:
            image_text = attrs.get('alt', '') or attrs.get('title', '')
            if image_text and not (self.cfg_deduplicate_captions and image_text == self.last_caption):
                self.current_line.content += '[{}]'.format(image_text)
                self.last_caption = image_text

    def end_ul(self):
        self.li_level -= 1
        self.li_counter.pop()

    def start_ol(self):
        self.li_counter.append(1)
        self.li_level += 1

    def end_ol(self):
        self.li_level -= 1
        self.li_counter.pop()

    def start_li(self):
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
        self.current_table.append(Table())

    def start_tr(self):
        self.current_table[-1].add_row()

    def start_td(self):
        self.current_table[-1].add_column()

    def end_td(self):
        self.__flush(force=True)

    def end_table(self):
        table = self.current_table.pop()
        self.__flush_verbatim(str(table))

    def newline(self):
        self.__flush(force=True)

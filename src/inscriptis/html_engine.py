#!/usr/bin/env python
# coding:utf-8
'''
Converts HTML to Text

Guiding principles:

 a. break lines only if we encounter a block element
 b. paddings:
'''
from itertools import chain

from inscriptis.css import CSS, CssParse, HtmlElement
from inscriptis.html_properties import Display, WhiteSpace, Line
from inscriptis.table_engine import Table

try:
    # python 2 compatibility
    from HTMLParser import HTMLParser
    unescape = HTMLParser().unescape
except ImportError:
    from html import unescape


class Inscriptis(object):

    UL_COUNTER = ('* ', '+ ', 'o ', '- ')
    UL_COUNTER_LEN = len(UL_COUNTER)

    DEFAULT_ELEMENT = HtmlElement()

    def __init__(self, html_tree, display_images=False, deduplicate_captions=False, display_links=False):
        '''
        ::param: display_images \
            whether to include image tiles/alt texts
        ::param: deduplicate_captions \
            whether to deduplicate captions such as image titles
            (many newspaper include images and video previews with
             identifical titles).
        ::param: display_links \
            whether to display link targets (e.g. `[Python](https://www.python.org)`)
        '''
        # setup config
        self.cfg_deduplicate_captions = deduplicate_captions

        # setup start and end tag call tables
        self.start_tag_handler_dict = {
            'table': self.start_table,
            'tr': self.start_tr,
            'td': self.start_td,
            'th': self.start_td,
            'ul': self.start_ul,
            'ol': self.start_ol,
            'li': self.start_li,
            'br': self.newline,
            'a': self.start_a if display_links else None,
            'img': self.start_img if display_images else None,
        }
        self.end_tag_handler_dict = {
            'table': self.end_table,
            'ul': self.end_ul,
            'ol': self.end_ol,
            'td': self.end_td,
            'th': self.end_td,
            'a': self.end_a if display_links else None,
        }

        # instance variables
        self.current_tag = [HtmlElement()]
        self.current_line = [Line()]
        self.next_line = [Line()]

        # the canvases used for displaying text
        # clean_text_line[0] refers to the root canvas; tables write into child
        # canvases that are created for every table line and merged with the
        # root canvas at the end of a table
        self.clean_text_lines = [[]]

        self.current_table = []
        self.li_counter = []
        self.li_level = 0
        self.invisible = []  # a list of attributes that are considered invisible
        self.last_caption = None

        # used if display_links is enabled
        self.link_target = ''

        # crawl the html tree
        self.crawl_tree(html_tree)
        if self.current_line[-1]:
            self.write_line()

    def crawl_tree(self, tree):
        if isinstance(tree.tag, str):
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
        return unescape('\n'.join(chain(*self.clean_text_lines))).rstrip()

    def write_line(self, force=False):
        '''
        Writes the current line to the buffer, provided that there is any
        data to write.

        ::returns:
            True, if a line has been writer, otherwise False
        '''
        # only break the line if there is any relevant content
        if not force and (not self.current_line[-1].content or self.current_line[-1].content.isspace()):
            self.current_line[-1].margin_before = max(self.current_line[-1].margin_before,
                                                      self.current_tag[-1].margin_before)
            return False

        line = self.current_line[-1].get_text()
        self.clean_text_lines[-1].append(line)
        self.current_line[-1] = self.next_line[-1]
        self.next_line[-1] = Line()
        return True

    def write_line_verbatim(self, text):
        '''
        Writes the current buffer without any modifications.
        '''
        self.clean_text_lines[-1].append(text)

    def handle_starttag(self, tag, attrs):
        # use the css to handle tags known to it :)

        cur = CSS.get(tag, Inscriptis.DEFAULT_ELEMENT)
        if 'style' in attrs:
            cur = CssParse.get_style_attribute(
                attrs['style'], html_element=cur)
        self.current_tag.append(cur)
        if cur.display == Display.none or self.invisible:
            self.invisible.append(cur)
            return

        self.next_line[-1].padding = self.current_line[-1].padding + cur.padding
        # flush text before display:block elements
        if cur.display == Display.block:
            if not self.write_line():
                self.current_line[-1].margin_before = max(
                    self.current_line[-1].margin_before, cur.margin_before)
                self.current_line[-1].padding = self.next_line[-1].padding
            else:
                self.current_line[-1].margin_after = max(
                    self.current_line[-1].margin_after, cur.margin_after)

        handler = self.start_tag_handler_dict.get(tag, None)
        if handler:
            handler(attrs)

    def handle_endtag(self, tag):
        cur = self.current_tag.pop()
        if self.invisible:
            self.invisible.pop()
            return

        self.next_line[-1].padding = self.current_line[-1].padding - cur.padding
        self.current_line[-1].margin_after = max(
            self.current_line[-1].margin_after, cur.margin_after)
        # flush text after display:block elements
        if cur.display == Display.block:
            # propagate the new padding to the current line, if nothing has
            # been written
            if not self.write_line():
                self.current_line[-1].padding = self.next_line[-1].padding

        handler = self.end_tag_handler_dict.get(tag, None)
        if handler:
            handler()

    def handle_data(self, data):
        if self.invisible:
            return

        # protect pre areas
        if self.current_tag[-1].whitespace == WhiteSpace.pre:
            data = '\0' + data + '\0'

        # determine whether to add this content to a table column
        # or to a standard line
        self.current_line[-1].content += data

    def start_ul(self, attrs):
        self.li_level += 1
        self.li_counter.append(Inscriptis.get_bullet(self.li_level - 1))

    def end_ul(self):
        self.li_level -= 1
        self.li_counter.pop()

    def start_img(self, attrs):
        image_text = attrs.get('alt', '') or attrs.get('title', '')
        if image_text and not (self.cfg_deduplicate_captions and image_text == self.last_caption):
            self.current_line[-1].content += '[{}]'.format(image_text)
            self.last_caption = image_text

    def start_a(self, attrs):
        self.link_target = attrs.get('href', '')
        self.current_line[-1].content += '['

    def end_a(self):
        self.current_line[-1].content += ']({})'.format(self.link_target)

    def start_ol(self, attrs):
        self.li_counter.append(1)
        self.li_level += 1

    def end_ol(self):
        self.li_level -= 1
        self.li_counter.pop()

    def start_li(self, attrs):
        self.write_line()
        if self.li_level > 0:
            bullet = self.li_counter[-1]
        else:
            bullet = "* "
        if isinstance(bullet, int):
            self.li_counter[-1] += 1
            self.current_line[-1].list_bullet = "{}. ".format(bullet)
        else:
            self.current_line[-1].list_bullet = bullet

    def start_table(self, attrs):
        self.current_table.append(Table())

    def start_tr(self, attrs):
        if self.current_table:
            # check whether we need to cleanup a <td> tag that has not been
            # closed yet
            if self.current_table[-1].td_is_open:
                self.end_td()

            self.current_table[-1].add_row()

    def start_td(self, attrs):
        if self.current_table:
            # check whether we need to cleanup a <td> tag that has not been
            # closed yet
            if self.current_table[-1].td_is_open:
                self.end_td()

            # open td tag
            self.clean_text_lines.append([])
            self.current_line.append(Line())
            self.next_line.append(Line())
            self.current_table[-1].add_cell(self.clean_text_lines[-1])
            self.current_table[-1].td_is_open = True

    def end_td(self):
        if self.current_table and self.current_table[-1].td_is_open:
            self.current_table[-1].td_is_open = False
            self.write_line(force=True)
            self.clean_text_lines.pop()
            self.current_line.pop()
            self.next_line.pop()

    def end_tr(self):
        pass

    def end_table(self):
        if self.current_table and self.current_table[-1].td_is_open:
            self.end_td()
        self.write_line()
        table = self.current_table.pop()
        self.write_line_verbatim(table.get_text())

    def newline(self, attrs):
        self.write_line(force=True)

    @staticmethod
    def get_bullet(index):
        '''
        ::return:
           the bullet that corresponds to the given index
        '''
        return Inscriptis.UL_COUNTER[index % Inscriptis.UL_COUNTER_LEN]

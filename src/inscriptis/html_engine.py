#!/usr/bin/env python
# coding:utf-8
'''
The HTML Engine is responsible for converting HTML to text.

Guiding principles:

 1. break lines only if we encounter a block element
'''
from itertools import chain
from html import unescape

from inscriptis.model.css import CssParse, HtmlElement
from inscriptis.model.canvas import Line
from inscriptis.model.config import ParserConfig
from inscriptis.model.table import Table
from inscriptis.html_properties import Display, WhiteSpace


class Inscriptis():
    '''
    The Inscriptis class translates an lxml HTML tree to the corresponding
    text representation.

    Args:
      html_tree: the lxml HTML tree to convert.
      config: an optional ParserConfig configuration object.

    Example::

      from lxml.html import fromstring
      from inscriptis.html_engine import Inscriptis

      html_content = "<html><body><h1>Test</h1></body></html>"

      # create an HTML tree from the HTML content.
      html_tree = fromstring(html_content)

      # transform the HTML tree to text.
      parser = Inscriptis(html_tree)
      text = parser.get_text()
    '''

    UL_COUNTER = ('* ', '+ ', 'o ', '- ')
    UL_COUNTER_LEN = len(UL_COUNTER)

    DEFAULT_ELEMENT = HtmlElement()

    def __init__(self, html_tree, config=None):
        # use the default configuration, if no config object is provided
        self.config = config or ParserConfig()

        # setup start and end tag call tables
        self.start_tag_handler_dict = {
            'table': self._start_table,
            'tr': self._start_tr,
            'td': self._start_td,
            'th': self._start_td,
            'ul': self._start_ul,
            'ol': self._start_ol,
            'li': self._start_li,
            'br': self._newline,
            'a': self._start_a if self.config.parse_a() else None,
            'img': self._start_img if self.config.display_images else None,
        }
        self.end_tag_handler_dict = {
            'table': self._end_table,
            'ul': self._end_ul,
            'ol': self._end_ol,
            'td': self._end_td,
            'th': self._end_td,
            'a': self._end_a if self.config.parse_a() else None,
        }

        # instance variables
        self.current_tag = [self.config.css['body']]
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
        self.last_caption = None

        # used if display_links is enabled
        self.link_target = ''

        # crawl the html tree
        self._parse_html_tree(html_tree)
        if self.current_line[-1]:
            self._write_line()

    def _parse_html_tree(self, tree):
        '''
        Parses the HTML tree.

        Args:
            tree: the HTML tree to parse.
        '''
        if isinstance(tree.tag, str):
            self.handle_starttag(tree.tag, tree.attrib)
            if tree.text:
                self.handle_data(tree.text)

            for node in tree:
                self._parse_html_tree(node)

            self.handle_endtag(tree.tag)

        if tree.tail:
            self.handle_data(tree.tail)

    def get_text(self):
        '''
        Returns:
          str -- A text representation of the parsed content.
        '''
        return unescape('\n'.join(chain(*self.clean_text_lines))).rstrip()

    def _write_line(self, force=False):
        '''
        Writes the current line to the buffer, provided that there is any
        data to write.

        Returns:
          bool -- True, if a line has been writer, otherwise False.
        '''
        # only break the line if there is any relevant content
        if not force and (not self.current_line[-1].content or
                          self.current_line[-1].content.isspace()):
            self.current_line[-1].margin_before = \
                max(self.current_line[-1].margin_before,
                    self.current_tag[-1].margin_before)
            return False

        line = self.current_line[-1].get_text()
        self.clean_text_lines[-1].append(line)
        self.current_line[-1] = self.next_line[-1]
        self.next_line[-1] = Line()
        return True

    def _write_line_verbatim(self, text):
        '''
        Writes the current buffer without any modifications.

        Args:
          text (str): the text to write.
        '''
        self.clean_text_lines[-1].append(text)

    def handle_starttag(self, tag, attrs):
        '''
        Handels HTML start tags.

        Args:
          tag (str): the HTML start tag to process.
          attrs (dict): a dictionary of HTML attributes and their respective
             values.
        '''
        # use the css to handle tags known to it :)

        cur = self.current_tag[-1].get_refined_html_element(
            self.config.css.get(tag, Inscriptis.DEFAULT_ELEMENT))
        if 'style' in attrs:
            cur = CssParse.get_style_attribute(
                attrs['style'], html_element=cur)
        self.current_tag.append(cur)

        self.next_line[-1].padding = self.current_line[-1].padding \
            + cur.padding
        # flush text before display:block elements
        if cur.display == Display.block:
            if not self._write_line():
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
        '''
        Handels HTML end tags.

        Args:
          tag(str): the HTML end tag to process.
        '''
        cur = self.current_tag.pop()
        self.next_line[-1].padding = self.current_line[-1].padding \
            - cur.padding
        self.current_line[-1].margin_after = max(
            self.current_line[-1].margin_after, cur.margin_after)
        # flush text after display:block elements
        if cur.display == Display.block:
            # propagate the new padding to the current line, if nothing has
            # been written
            if not self._write_line():
                self.current_line[-1].padding = self.next_line[-1].padding

        handler = self.end_tag_handler_dict.get(tag, None)
        if handler:
            handler()

    def handle_data(self, data):
        '''
        Handels text belonging to HTML tags.

        Args:
          data (str): The text to process.
        '''
        if self.current_tag[-1].display == Display.none:
            return

        # protect pre areas
        if self.current_tag[-1].whitespace == WhiteSpace.pre:
            data = '\0' + data + '\0'

        # add prefix, if present
        data = self.current_tag[-1].prefix + data + self.current_tag[-1].suffix

        # determine whether to add this content to a table column
        # or to a standard line
        self.current_line[-1].content += data

    def _start_ul(self, attrs):
        self.li_level += 1
        self.li_counter.append(Inscriptis.get_bullet(self.li_level - 1))

    def _end_ul(self):
        self.li_level -= 1
        self.li_counter.pop()

    def _start_img(self, attrs):
        image_text = attrs.get('alt', '') or attrs.get('title', '')
        if image_text and not (self.config.deduplicate_captions and
                               image_text == self.last_caption):
            self.current_line[-1].content += '[{}]'.format(image_text)
            self.last_caption = image_text

    def _start_a(self, attrs):
        self.link_target = ''
        if self.config.display_links:
            self.link_target = attrs.get('href', '')
        if self.config.display_anchors:
            self.link_target = self.link_target or attrs.get('name', '')

        if self.link_target:
            self.current_line[-1].content += '['

    def _end_a(self):
        if self.link_target:
            self.current_line[-1].content += ']({})'.format(self.link_target)

    def _start_ol(self, attrs):
        self.li_counter.append(1)
        self.li_level += 1

    def _end_ol(self):
        self.li_level -= 1
        self.li_counter.pop()

    def _start_li(self, attrs):
        self._write_line()
        if self.li_level > 0:
            bullet = self.li_counter[-1]
        else:
            bullet = "* "
        if isinstance(bullet, int):
            self.li_counter[-1] += 1
            self.current_line[-1].list_bullet = "{}. ".format(bullet)
        else:
            self.current_line[-1].list_bullet = bullet

    def _start_table(self, attrs):
        self.current_table.append(Table())

    def _start_tr(self, attrs):
        if self.current_table:
            # check whether we need to cleanup a <td> tag that has not been
            # closed yet
            if self.current_table[-1].td_is_open:
                self._end_td()

            self.current_table[-1].add_row()

    def _start_td(self, attrs):
        if self.current_table:
            # check whether we need to cleanup a <td> tag that has not been
            # closed yet
            if self.current_table[-1].td_is_open:
                self._end_td()

            # open td tag
            self.clean_text_lines.append([])
            self.current_line.append(Line())
            self.next_line.append(Line())
            self.current_table[-1].add_cell(self.clean_text_lines[-1])
            self.current_table[-1].td_is_open = True

    def _end_td(self):
        if self.current_table and self.current_table[-1].td_is_open:
            self.current_table[-1].td_is_open = False
            self._write_line(force=True)
            self.clean_text_lines.pop()
            self.current_line.pop()
            self.next_line.pop()

    def _end_tr(self):
        pass

    def _end_table(self):
        if self.current_table and self.current_table[-1].td_is_open:
            self._end_td()
        self._write_line()
        table = self.current_table.pop()
        self._write_line_verbatim(table.get_text())

    def _newline(self, attrs):
        self._write_line(force=True)

    @staticmethod
    def get_bullet(index):
        '''
        Returns:
          str -- The bullet that corresponds to the given index.
        '''
        return Inscriptis.UL_COUNTER[index % Inscriptis.UL_COUNTER_LEN]

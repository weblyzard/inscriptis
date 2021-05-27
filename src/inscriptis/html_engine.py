#!/usr/bin/env python
# coding:utf-8
"""
The HTML Engine is responsible for converting HTML to text.

Guiding principles:

 1. break lines only if we encounter a block element
"""
from copy import copy

from inscriptis.annotation.helper import AnnotationHelper
from inscriptis.html_properties import Display
from inscriptis.model.attribute import apply_attributes
from inscriptis.model.html_element import HtmlElement
from inscriptis.model.canvas import Canvas
from inscriptis.model.config import ParserConfig
from inscriptis.model.table import Table


class Inscriptis:
    """
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
    """

    UL_COUNTER = ('* ', '+ ', 'o ', '- ')
    UL_COUNTER_LEN = len(UL_COUNTER)

    DEFAULT_ELEMENT = HtmlElement()

    def __init__(self, html_tree, config=None):
        # use the default configuration, if no config object is provided
        self.config = config or ParserConfig()
        self.annotations = AnnotationHelper()

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
        self.canvas = Canvas()
        self.tags = [self.config.css['body'].set_canvas(self.canvas)]

        self.current_table = []
        self.li_counter = []
        self.li_level = 0
        self.last_caption = None

        # used if display_links is enabled
        self.link_target = ''

        # crawl the html tree
        self._parse_html_tree(html_tree)

    def _parse_html_tree(self, tree):
        """
        Parses the HTML tree.

        Args:
            tree: the HTML tree to parse.
        """
        # ignore comments
        if not isinstance(tree.tag, str):
            return

        self.handle_starttag(tree.tag, tree.attrib)
        self.tags[-1].write(tree.text)

        for node in tree:
            self._parse_html_tree(node)

        self.handle_endtag(tree.tag)
        prev = self.tags.pop()

        # write the tail text to the element's container
        self.tags[-1].write_tail(tree.tail, is_close_block=(prev.display == Display.block))

    def get_text(self):
        """
        Returns:
          str -- A text representation of the parsed content.
        """
        return self.canvas.get_text().rstrip()

    def handle_starttag(self, tag, attrs):
        """
        Handles HTML start tags.

        Args:
          tag (str): the HTML start tag to process.
          attrs (dict): a dictionary of HTML attributes and their respective
             values.
        """
        # use the css to handle tags known to it :)

        cur = self.tags[-1].get_refined_html_element(
            apply_attributes(attrs, html_element=copy(self.config.css.get(
                tag, Inscriptis.DEFAULT_ELEMENT))).set_tag(tag))
        self.tags.append(cur)

        #self.next_line[-1].padding = self.current_line[-1].padding \
        #    + cur.padding

        # flush text before display:block elements
        #if cur.display == Display.block:
        #    if not self._write_line():
        #        self.current_line[-1].margin_before = 0 \
        #            if not self.clean_text_lines[0] else max(
        #                self.current_line[-1].margin_before, cur.margin_before)
        #        self.current_line[-1].padding = self.next_line[-1].padding
        #    else:
        #        self.current_line[-1].margin_after = max(
        #            self.current_line[-1].margin_after, cur.margin_after)

        handler = self.start_tag_handler_dict.get(tag, None)
        if handler:
            handler(attrs)

    def handle_endtag(self, tag):
        """
        Handles HTML end tags.

        Args:
          tag(str): the HTML end tag to process.
        """
        handler = self.end_tag_handler_dict.get(tag, None)
        if handler:
            handler()

    def _start_ul(self, attrs):
        self.li_level += 1
        self.li_counter.append(Inscriptis.get_bullet(self.li_level - 1))

    def _end_ul(self):
        self.li_level -= 1
        self.li_counter.pop()

    def _start_img(self, attrs):
        image_text = attrs.get('alt', '') or attrs.get('title', '')
        if image_text and not (self.config.deduplicate_captions
                               and image_text == self.last_caption):
            self.tags[-1].write('[{0}]'.format(image_text))
            self.last_caption = image_text

    def _start_a(self, attrs):
        self.link_target = ''
        if self.config.display_links:
            self.link_target = attrs.get('href', '')
        if self.config.display_anchors:
            self.link_target = self.link_target or attrs.get('name', '')

        if self.link_target:
            self.tags[-1].write('[')

    def _end_a(self):
        if self.link_target:
            self.tags[-1].write(']({0})'.format(self.link_target))

    def _start_ol(self, attrs):
        self.li_counter.append(1)
        self.li_level += 1

    def _end_ol(self):
        self.li_level -= 1
        self.li_counter.pop()

    def _start_li(self, attrs):
        if self.li_level > 0:
            bullet = self.li_counter[-1]
        else:
            bullet = "* "
        if isinstance(bullet, int):
            self.li_counter[-1] += 1
            self.tags[-1].list_bullet = "{0}. ".format(bullet)
        else:
            self.tags[-1].list_bullet = bullet

        self.tags[-1].write('')

    def _start_table(self, attrs):
        self.tags[-1].set_canvas(Canvas())
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
            # self.clean_text_lines.append([])
            # self.current_line.append(Line())
            # self.next_line.append(Line())
            canvas = self.tags[-1].set_canvas(Canvas()).canvas
            self.current_table[-1].add_cell(canvas,
                                            align=self.tags[-1].align,
                                            valign=self.tags[-1].valign)
            self.current_table[-1].td_is_open = True

    def _end_td(self):
        if self.current_table and self.current_table[-1].td_is_open:
            self.current_table[-1].td_is_open = False
            self.tags[-1].close_block()
            # self._write_line(force=True)
            # self.clean_text_lines.pop()
            # self.current_line.pop()
            # self.next_line.pop()

    def _end_tr(self):
        pass

    def _end_table(self):
        if self.current_table and self.current_table[-1].td_is_open:
            self._end_td()
        # self._write_line()
        table = self.current_table.pop()
        self.tags[-2].write_verbatim_text(table.get_text())

    def _newline(self, attrs):
        self.tags[-1].write_verbatim_text('\n')

    @staticmethod
    def get_bullet(index):
        """
        Returns:
          str -- The bullet that corresponds to the given index.
        """
        return Inscriptis.UL_COUNTER[index % Inscriptis.UL_COUNTER_LEN]
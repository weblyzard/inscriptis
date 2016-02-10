#!/usr/bin/env python
# coding: utf-8

'''
Handeling of CSS files.
'''

from inscriptis.html_properties import Display, WhiteSpace
from re import compile as re_compile

class HtmlElement(object):

    __slots__ = ('tag', 'prefix', 'suffix', 'display', 'margin_before',
                 'margin_after', 'padding', 'whitespace')

    def __init__(self, tag='/', prefix='', suffix='', display=Display.inline, \
            margin_before=0, margin_after=0, padding=0, whitespace=WhiteSpace.normal):
        self.tag = tag
        self.prefix = prefix
        self.suffix = suffix
        self.display = display
        self.margin_before = margin_before
        self.margin_after = margin_after
        self.padding = padding
        self.whitespace = whitespace

    def clone(self):
        '''
        ::return: \
            a clone of the current HtmlElement
        '''
        return HtmlElement(self.tag, self.prefix, self.suffix, self.display,
                           self.margin_before, self.margin_after, self.padding,
                           self.whitespace)

    def __str__(self):
        return "<{tag} prefix={prefix}, suffix={suffix}, display={display}, " \
               "margin_before={margin_before}, margin_after={margin_after}, " \
               "padding={padding}, whitespace={whitespace}>".format( \
                  tag=self.tag, \
                  prefix=self.prefix, \
                  suffix=self.suffix, \
                  display=self.display, \
                  margin_before=self.margin_before, \
                  margin_after=self.margin_after, \
                  padding=self.padding, \
                  whitespace=self.whitespace)

class CssParse(object):
    '''
    Translates css directives into the corresponding HtmlElements.

    The attribute `display: none`, for instance, is translated to
    `HtmlElement.display=Display.none`.
    '''
    # used to separate value and unit from each other
    RE_UNIT = re_compile(r'(\d+)(\w+)')

    @staticmethod
    def get_style_attribute(style_attribute, html_element):
        '''
        ::param: style_directive \
          The attribute value of the given style sheet.
          Example: display: none

        ::param: html_element: \
          The HtmlElement to which the given style is applied

        ::returns:
            A HtmlElement that merges the given element with
            the style attributes specified.
        '''
        custome_html_element = html_element.clone()
        for style_directive in style_attribute.lower().split(';'):
            if not ':' in style_directive:
                continue
            key, value = (s.strip() for s in style_directive.split(':', 1))

            try:
                apply_style = getattr(CssParse, "_attr_" + \
                        key.replace('-webkit-', '').replace("-", "_"))
                apply_style(value, custome_html_element)
            except AttributeError:
                pass

        return custome_html_element


    @staticmethod
    def _get_em(length):
        '''
        ::param: length \
            the length specified in the CSS.

        ::return:
            the length in em's.
        '''
        m = CssParse.RE_UNIT.search(length)
        value = int(m.group(1))
        unit = m.group(2)

        if unit not in ('em', 'qem', 'rem'):
            value = int(round(value/8))
        return value

    # ------------------------------------------------------------------------
    # css styles
    # ------------------------------------------------------------------------

    @staticmethod
    def _attr_display(value, html_element):
        '''
        Set the display value
        '''
        if value == 'block':
            html_element.display = Display.block
        elif value == 'none':
            html_element.display = Display.none
        else:
            html_element.display = Display.inline

    @staticmethod
    def _attr_margin_top(value, html_element):
        html_element.margin_before = CssParse._get_em(value)

    @staticmethod
    def _attr_margin_bottom(value, html_element):
        html_element.margin_after = CssParse._get_em(value)

    @staticmethod
    def _attr_padding_left(value, html_element):
        html_element.padding = CssParse._get_em(value)


    # register aliases
    _attr_margin_before = _attr_margin_top
    _attr_margin_after = _attr_margin_bottom
    _attr_padding_start = _attr_padding_left


CSS = {
    'head': HtmlElement('head', display=Display.none),
    'link': HtmlElement('link', display=Display.none),
    'meta': HtmlElement('meta', display=Display.none),
    'script': HtmlElement('script', display=Display.none),
    'title': HtmlElement('title', display=Display.none),
    'style': HtmlElement('style', display=Display.none),

    'p': HtmlElement('p', display=Display.block, margin_before=1, margin_after=1),
    'figure': HtmlElement('figure', display=Display.block, margin_before=1, margin_after=1),


    'h1': HtmlElement('h1', display=Display.block, margin_before=1, margin_after=1),
    'h2': HtmlElement('h2', display=Display.block, margin_before=1, margin_after=1),
    'h3': HtmlElement('h3', display=Display.block, margin_before=1, margin_after=1),
    'h4': HtmlElement('h4', display=Display.block, margin_before=1, margin_after=1),
    'h5': HtmlElement('h5', display=Display.block, margin_before=1, margin_after=1),
    'h6': HtmlElement('h6', display=Display.block, margin_before=1, margin_after=1),

    'ul': HtmlElement('ul', display=Display.block, margin_before=0, margin_after=0, padding=4),
    'ol': HtmlElement('ol', display=Display.block, margin_before=0, margin_after=0, padding=4),
    'li': HtmlElement('li', display=Display.block),

    'address': HtmlElement('address', display=Display.block),
    'article': HtmlElement('article', display=Display.block),
    'aside': HtmlElement('aside', display=Display.block),
    'div': HtmlElement('div', display=Display.block),
    'footer': HtmlElement('footer', display=Display.block),
    'header': HtmlElement('header', display=Display.block),
    'hgroup': HtmlElement('hgroup', display=Display.block),
    'layer': HtmlElement('layer', display=Display.block),
    'main': HtmlElement('main', display=Display.block),
    'nav': HtmlElement('nav', display=Display.block),
    'figcaption': HtmlElement('figcaption', display=Display.block),

    'blockquote': HtmlElement('blockquote', display=Display.block),

    'q': HtmlElement('q', prefix='"', suffix='"'),
    'span': HtmlElement('span', ),
}

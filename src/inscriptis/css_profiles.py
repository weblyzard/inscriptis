#!/usr/bin/env python3
# coding: utf-8
'''
Standard CSS profiles shipped with inscriptis.

- `strict`: this profile corresponds to the defaults used by Firefox
- `relaxed`: this profile is more suited for text analytics, since it ensures
             that whitespaces are inserted between span and div elements
             preventing cases where two words stick together.
'''

from inscriptis.model.css import HtmlElement
from inscriptis.html_properties import Display, WhiteSpace

STRICT_CSS_PROFILE = {
    'body': HtmlElement('body', display=Display.inline,
                        whitespace=WhiteSpace.normal),
    'head': HtmlElement('head', display=Display.none),
    'link': HtmlElement('link', display=Display.none),
    'meta': HtmlElement('meta', display=Display.none),
    'script': HtmlElement('script', display=Display.none),
    'title': HtmlElement('title', display=Display.none),
    'style': HtmlElement('style', display=Display.none),

    'p': HtmlElement('p', display=Display.block, margin_before=1,
                     margin_after=1),
    'figure': HtmlElement('figure', display=Display.block, margin_before=1,
                          margin_after=1),

    'h1': HtmlElement('h1', display=Display.block, margin_before=1,
                      margin_after=1),
    'h2': HtmlElement('h2', display=Display.block, margin_before=1,
                      margin_after=1),
    'h3': HtmlElement('h3', display=Display.block, margin_before=1,
                      margin_after=1),
    'h4': HtmlElement('h4', display=Display.block, margin_before=1,
                      margin_after=1),
    'h5': HtmlElement('h5', display=Display.block, margin_before=1,
                      margin_after=1),
    'h6': HtmlElement('h6', display=Display.block, margin_before=1,
                      margin_after=1),

    'ul': HtmlElement('ul', display=Display.block, margin_before=0,
                      margin_after=0, padding=4),
    'ol': HtmlElement('ol', display=Display.block, margin_before=0,
                      margin_after=0, padding=4),
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

    # Handling of <pre>
    'pre': HtmlElement('pre', display=Display.block,
                       whitespace=WhiteSpace.pre),
}

RELAXED_CSS_PROFILE = STRICT_CSS_PROFILE.copy()
RELAXED_CSS_PROFILE['div'] = HtmlElement('div', display=Display.block,
                                         padding=2)
RELAXED_CSS_PROFILE['span'] = HtmlElement('span', display=Display.inline,
                                          prefix=' ', suffix=' ',
                                          limit_whitespace_affixes=True)


CSS_PROFILES = {'strict': STRICT_CSS_PROFILE,
                'relaxed': RELAXED_CSS_PROFILE}

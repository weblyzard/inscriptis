#!/usr/bin/env python3
# coding: utf-8
"""Standard CSS profiles shipped with inscriptis.

- `strict`: this profile corresponds to the defaults used by Firefox
- `relaxed`: this profile is more suited for text analytics, since it ensures
             that whitespaces are inserted between span and div elements
             preventing cases where two words stick together.
"""

from inscriptis.html_properties import Display, WhiteSpace
from inscriptis.model.html_element import HtmlElement

STRICT_CSS_PROFILE = {
    "body": HtmlElement(display=Display.inline, whitespace=WhiteSpace.normal),
    "head": HtmlElement(display=Display.none),
    "link": HtmlElement(display=Display.none),
    "meta": HtmlElement(display=Display.none),
    "script": HtmlElement(display=Display.none),
    "title": HtmlElement(display=Display.none),
    "style": HtmlElement(display=Display.none),
    "p": HtmlElement(display=Display.block, margin_before=1, margin_after=1),
    "figure": HtmlElement(display=Display.block, margin_before=1, margin_after=1),
    "h1": HtmlElement(display=Display.block, margin_before=1, margin_after=1),
    "h2": HtmlElement(display=Display.block, margin_before=1, margin_after=1),
    "h3": HtmlElement(display=Display.block, margin_before=1, margin_after=1),
    "h4": HtmlElement(display=Display.block, margin_before=1, margin_after=1),
    "h5": HtmlElement(display=Display.block, margin_before=1, margin_after=1),
    "h6": HtmlElement(display=Display.block, margin_before=1, margin_after=1),
    "ul": HtmlElement(
        display=Display.block, margin_before=0, margin_after=0, padding_inline=4
    ),
    "ol": HtmlElement(
        display=Display.block, margin_before=0, margin_after=0, padding_inline=4
    ),
    "li": HtmlElement(display=Display.block),
    "address": HtmlElement(display=Display.block),
    "article": HtmlElement(display=Display.block),
    "aside": HtmlElement(display=Display.block),
    "div": HtmlElement(display=Display.block),
    "footer": HtmlElement(display=Display.block),
    "header": HtmlElement(display=Display.block),
    "hgroup": HtmlElement(display=Display.block),
    "layer": HtmlElement(display=Display.block),
    "main": HtmlElement(display=Display.block),
    "nav": HtmlElement(display=Display.block),
    "figcaption": HtmlElement(display=Display.block),
    "blockquote": HtmlElement(display=Display.block),
    "q": HtmlElement(prefix='"', suffix='"'),
    # Handling of <pre>
    "pre": HtmlElement(display=Display.block, whitespace=WhiteSpace.pre),
    "xmp": HtmlElement(display=Display.block, whitespace=WhiteSpace.pre),
    "listing": HtmlElement(display=Display.block, whitespace=WhiteSpace.pre),
    "plaintext": HtmlElement(display=Display.block, whitespace=WhiteSpace.pre),
}

RELAXED_CSS_PROFILE = STRICT_CSS_PROFILE.copy()
RELAXED_CSS_PROFILE["div"] = HtmlElement(display=Display.block, padding_inline=2)
RELAXED_CSS_PROFILE["span"] = HtmlElement(
    display=Display.inline, prefix=" ", suffix=" ", limit_whitespace_affixes=True
)


CSS_PROFILES = {"strict": STRICT_CSS_PROFILE, "relaxed": RELAXED_CSS_PROFILE}

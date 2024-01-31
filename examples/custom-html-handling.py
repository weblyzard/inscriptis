#!/usr/bin/env python3

"""
Custom HTML tag handling example.

Add a custom HTML handler for the bold <b> tag which encloses
bold text with "**".

Example:
    "Welcome to <b>Chur</b>" is rendered as "Welcome to **Chur**".
"""


from inscriptis.html_engine import Inscriptis
from functools import partial
from lxml.html import fromstring


def my_handle_start_b(self, attrs):
    """Handle the opening <b> tag."""
    self.tags[-1].write("**")


def my_handle_end_b(self):
    """Handle the closing </b> tag."""
    self.tags[-1].write("**")


HTML = "Welcome to <b>Chur</b>"

html_tree = fromstring(HTML)
inscriptis = Inscriptis(html_tree)
inscriptis.start_tag_handler_dict["b"] = partial(my_handle_start_b, inscriptis)
inscriptis.end_tag_handler_dict["b"] = partial(my_handle_end_b, inscriptis)
print(inscriptis.get_text())

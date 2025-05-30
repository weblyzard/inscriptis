#!/usr/bin/env python

"""ensures that xml declaration headers are correctly stripped"""

from inscriptis import get_text


def test_successive_a():
    html = '<?xml version="1.0" encoding="UTF-8" ?> Hallo?>'
    assert get_text(html).strip() == "Hallo?>"

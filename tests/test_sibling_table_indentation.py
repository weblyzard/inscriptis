#!/usr/bin/env python

"""
Ensure that sibling tables do not accumulate indentation of their parent.

Verifies the fix for https://github.com/weblyzard/inscriptis/security/advisories/GHSA-q87h-c5m7-659j
"""

from inscriptis import get_text


def test_sibling_tables_keep_indentation():
    html = "<ul>" + "<table><tr><td>a</td></tr></table>" * 4 + "</ul>"
    lines = [line for line in get_text(html).split("\n") if line.strip()]
    assert len(lines) == 4
    assert len({len(line) for line in lines}) == 1


def test_sibling_tables_output_is_linear():
    html = "<div>" + "<table></table>" * 2000 + "</div>"
    assert len(get_text(html)) < 20 * 2000


def test_table_annotation_offsets_are_not_shifted_by_padding():
    """A table inside a padded block must keep annotation offsets aligned."""
    from inscriptis import get_annotated_text
    from inscriptis.model.config import ParserConfig

    html = '<div style="padding-left:4em"><table><tr><td><b>A</b></td></tr></table></div>'
    result = get_annotated_text(html, ParserConfig(annotation_rules={"b": ["b"]}))
    assert result["label"]
    for start, end, _ in result["label"]:
        assert result["text"][start:end] == "A"

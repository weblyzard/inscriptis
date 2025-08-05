#!/usr/bin/env python

"""
Test the annotation output formatter.
"""

import pytest

from inscriptis.annotation.output import AnnotationProcessor
from inscriptis.annotation.output.html import HtmlExtractor
from inscriptis.annotation.output.surface import SurfaceExtractor
from inscriptis.annotation.output.xml import XmlExtractor

EXAMPLE_OUTPUT = {
    "text": "Chur\n\nChur is the capital and largest town of "
    "the Swiss canton of the Grisons and lies in the "
    "Grisonian Rhine Valley.",
    "label": [[0, 4, "h1"], [0, 4, "heading"], [6, 10, "emphasis"]],
}


def test_abstract_class():
    processor = AnnotationProcessor()

    with pytest.raises(NotImplementedError):
        _ = processor(EXAMPLE_OUTPUT)


def test_surface_annotator():
    processor = SurfaceExtractor()
    result = processor(EXAMPLE_OUTPUT)

    # the old keys haven't been changed
    assert "text" in result
    assert "label" in result

    # and we have additional information on surface forms :)
    assert result["surface"] == [
        ("h1", "Chur"),
        ("heading", "Chur"),
        ("emphasis", "Chur"),
    ]


def test_xml_annotator():
    processor = XmlExtractor()
    result = processor(EXAMPLE_OUTPUT)

    # and we have additional information on surface forms :)
    assert result == (
        '<?xml version="1.0" encoding="UTF-8" ?>\n<content>\n'
        "<heading><h1>Chur</h1></heading>\n\n<emphasis>"
        "Chur</emphasis> is the capital and largest town "
        "of the Swiss canton of the Grisons and lies in "
        "the Grisonian Rhine Valley.\n</content>"
    )


def test_html_annotator():
    processor = HtmlExtractor()
    result = processor(EXAMPLE_OUTPUT)

    assert result.startswith("<html><head><style>")
    assert result.split("</style>")[1] == (
        "</head>"
        '<body><pre><span class="heading-label">heading'
        '</span><span class="heading">'
        '<span class="h1-label">h1</span><span class="h1">'
        "Chur</span></span></pre>\n"
        "<pre></pre>\n"
        '<pre><span class="emphasis-label">emphasis</span>'
        '<span class="emphasis">Chur</span> is the capital '
        "and largest town of the Swiss canton of the "
        "Grisons and lies in the Grisonian Rhine Valley."
        "</pre></body></html>"
    )


def test_trailing_tag_annotation():
    processor = XmlExtractor()
    result = processor({"text": "Ehre sei Gott!", "label": [[9, 14, "emphasis"]]})

    assert result == (
        '<?xml version="1.0" encoding="UTF-8" ?>\n<content>\nEhre sei <emphasis>Gott!</emphasis>\n</content>'
    )

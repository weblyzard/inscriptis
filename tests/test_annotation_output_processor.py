#!/usr/bin/env python

"""
Test the annotation output formatter.
"""

import pytest

from inscriptis.annotation.output import AnnotationProcessor
from inscriptis.annotation.output.surface import SurfaceExtractor
from inscriptis.annotation.output.xml import XmlExtractor

EXAMPLE_OUTPUT = {'text': 'Chur\n\nChur is the capital and largest town of '
                          'the Swiss canton of the Grisons and lies in the '
                          'Grisonian Rhine Valley.',
                  'label': [[0, 4, 'heading'],
                            [0, 4, 'h1'],
                            [6, 10, 'emphasis']]}


def test_abstract_class():
    processor = AnnotationProcessor()

    with pytest.raises(NotImplementedError):
        result = processor(EXAMPLE_OUTPUT)

def test_surface_annotator():
    processor = SurfaceExtractor()
    result = processor(EXAMPLE_OUTPUT)

    # the old keys haven't been changed
    assert 'text' in result
    assert 'label' in result

    # and we have additional information on surface forms :)
    assert result['surface'] == [('heading', 'Chur'),
                                 ('h1', 'Chur'),
                                 ('emphasis', 'Chur')]

def test_xml_annotator():
    processor = XmlExtractor()
    result = processor(EXAMPLE_OUTPUT)

    # and we have additional information on surface forms :)
    assert result == ('<?xml version="1.0" encoding="UTF-8" ?>'
                      '<h1><heading>Chur</heading></h1>\n\n<emphasis>'
                      'Chur</emphasis> is the capital and largest town '
                      'of the Swiss canton of the Grisons and lies in '
                      'the Grisonian Rhine Valley.')

def test_trailing_tag_annotation():
    processor = XmlExtractor()
    result = processor({'text': 'Ehre sei Gott!',
                        'label': [[9, 14, 'emphasis']]})

    assert result == ('<?xml version="1.0" encoding="UTF-8" ?>'
                      'Ehre sei <emphasis>Gott!</emphasis>')


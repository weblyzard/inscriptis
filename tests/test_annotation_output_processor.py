#!/usr/bin/env python

"""
Test the annotation output formatter.
"""

import pytest

from inscriptis.annotation.output import AnnotationProcessor
from inscriptis.annotation.output.surface import SurfaceExtractor
from inscriptis.annotation.output.tag import TagExtractor

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

def test_tag_annotator():
    processor = TagExtractor()
    result = processor(EXAMPLE_OUTPUT)

    # the old keys haven't been changed
    assert 'text' in result
    assert 'label' in result

    # and we have additional information on surface forms :)
    assert result['tag'] == ('<h1><heading>Chur</heading></h1>\n\n<emphasis>'
                             'Chur</emphasis> is the capital and largest town '
                             'of the Swiss canton of the Grisons and lies in '
                             'the Grisonian Rhine Valley.')

def test_trailing_tag_annotation():
    processor = TagExtractor()
    result = processor({'text': 'Ehre sei Gott!',
                        'label': [[9, 14, 'emphasis']]})

    assert result['tag'] == 'Ehre sei <emphasis>Gott!</emphasis>'


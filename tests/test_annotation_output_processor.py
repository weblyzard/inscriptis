#!/usr/bin/env python

"""
Test the annotation output formatter.
"""

import pytest

from inscriptis.annotation.output import AnnotationProcessor
from inscriptis.annotation.output.surface import SurfaceExtractor

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
    assert result['surface_form'] == [('heading', 'Chur'),
                                      ('h1', 'Chur'),
                                      ('emphasis', 'Chur')]

#!/usr/bin/env python

"""
This test case verifies that annotation are correctly computed.
"""
import os
from json import load, loads
from glob import glob

from inscriptis.engine import get_jsonl
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

TESTCASE_PATTERN = os.path.join(os.path.dirname(__file__), 'html/*.json')


def test_html_annotations(filter_str=''):
    for annotation_file in glob(TESTCASE_PATTERN):
        if filter_str not in annotation_file:
            continue

        with open(annotation_file) as f:
            reference_annotations = load(f)

        with open(annotation_file.replace('.json', '.html')) as f:
            print(f.name)
            html = '<html><body>{}</body></html>'.format(f.read())

        result = loads(get_jsonl(html, ParserConfig(
            css=CSS_PROFILES['strict'],
            annotation_rules={'h1': ('heading', ),
                              'h2': ('heading', ),
                              'h3': ('heading', ),
                              'b': ('emphasis', ),
                              'table': ('table', )})))
        converted = [[a[2], result['text'][a[0]:a[1]]]
                     for a in result['label']]

        print("Reference:")
        print(reference_annotations)
        print("\nConverted:")
        print(converted)
        assert reference_annotations == converted


if __name__ == '__main__':
    from sys import argv

    filter_str = argv[1] if len(argv) > 1 else ''
    test_html_annotations(filter_str)

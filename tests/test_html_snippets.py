#!/usr/bin/env python

''' ensures that two successive <a>text</a> contain
    a space between each other, if there is a linebreak
    or space between the tags.
'''
from os.path import dirname, join
from glob import glob

from inscriptis import get_text
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

TESTCASE_PATTERN = join(dirname(__file__), 'html/*.txt')


def test_html_snippets(filter_str=''):
    for testcase_txt in glob(TESTCASE_PATTERN):
        if filter_str not in testcase_txt:
            continue

        with open(testcase_txt) as f:
            reference_txt = f.read().rstrip()

        with open(testcase_txt.replace(".txt", ".html")) as f:
            print(f.name)
            html = "<html><body>{}</body></html>".format(f.read())

        converted_txt = get_text(html, ParserConfig(
            css=CSS_PROFILES['strict'])).rstrip()

        if converted_txt != reference_txt:
            print("File:{}\nHTML:\n{}\n\nReference:\n{}\n\nConverted:\n{}"
                  .format(testcase_txt, html, reference_txt, converted_txt))

        assert converted_txt == reference_txt


if __name__ == '__main__':
    from sys import argv
    filter_str = argv[1] if len(argv) > 1 else ''
    test_html_snippets(filter_str)

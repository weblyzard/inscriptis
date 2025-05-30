#!/usr/bin/env python

"""
Test HTML snippets in the project's HTML directory. The corresponding .txt file
contains the reference conversion.
"""

from glob import glob
from os.path import dirname, join

from inscriptis import get_text
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

TESTCASE_PATTERN = join(dirname(__file__), "html/*.txt")


def test_html_snippets(filter_str=""):
    for testcase_txt in glob(TESTCASE_PATTERN):
        if filter_str not in testcase_txt:
            continue

        with open(testcase_txt) as f:
            reference_txt = f.read().rstrip()

        with open(testcase_txt.replace(".txt", ".html")) as f:
            print(f.name)
            html = f"<html><body>{f.read()}</body></html>"

        converted_txt = get_text(html, ParserConfig(css=CSS_PROFILES["strict"])).rstrip()

        if converted_txt != reference_txt:
            print(f"File:{testcase_txt}\nHTML:\n{html}\n\nReference:\n{reference_txt}\n\nConverted:\n{converted_txt}")
            print("HTML file:", testcase_txt.replace(".txt", ".html"))
            print("Visualize differences with `vimdiff reference.txt converted.txt`")
            with open("reference.txt", "w") as f:
                f.write(reference_txt)
            with open("converted.txt", "w") as f:
                f.write(converted_txt)

        assert converted_txt == reference_txt


if __name__ == "__main__":
    from sys import argv

    filter_str = argv[1] if len(argv) > 1 else ""
    test_html_snippets(filter_str)

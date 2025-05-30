#!/usr/bin/env python

"""
This test case verifies that annotation are correctly computed.
"""

import os
from glob import glob
from json import load

from inscriptis import get_annotated_text
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.config import ParserConfig

TESTCASE_PATTERN = os.path.join(os.path.dirname(__file__), "html/*.json")


def assert_equal_ignoring_whitespace(reference: list[str], converted: list[str]) -> bool:
    for (ref_tag, ref_str), (conv_tag, conv_str) in zip(reference, converted, strict=False):
        assert ref_tag == conv_tag
        assert "".join(ref_str.split()) == "".join(conv_str.split())


def test_html_annotations(filter_str=""):
    for annotation_file in glob(TESTCASE_PATTERN):
        if filter_str not in annotation_file:
            continue

        with open(annotation_file) as f:
            reference = load(f)

        with open(annotation_file.replace(".json", ".html")) as f:
            print(f.name)
            html = f"<html><body>{f.read()}</body></html>"

        for indentation_strategy in ("strict", "relaxed"):
            result = get_annotated_text(
                html,
                ParserConfig(
                    css=CSS_PROFILES[indentation_strategy],
                    annotation_rules=reference["annotation_rules"],
                ),
            )

            converted = [[a[2], result["text"][a[0] : a[1]]] for a in result["label"]]

            if reference["result"] != converted:
                print("Reference:")
                print(reference["result"])
                print(f"\nConverted (indentation strategy: {indentation_strategy})")
                print(converted)

            if indentation_strategy == "strict":
                assert reference["result"] == converted
            else:
                assert_equal_ignoring_whitespace(reference["result"], converted)


if __name__ == "__main__":
    from sys import argv

    filter_str = argv[1] if len(argv) > 1 else ""
    test_html_annotations(filter_str)

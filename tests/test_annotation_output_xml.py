#!/usr/bin/env python

"""
Test the annotation XmlExtractor.
"""

from lxml.html import fromstring

from inscriptis import Inscriptis
from inscriptis.annotation.output.xml import XmlExtractor
from inscriptis.model.config import ParserConfig


def test_tag_error_issue_93():
    """
    Test for the correct tag order in the XmlOutput as described in Issue #93.
    """
    html_issue_93 = """<html>
       <body>
         <div class="a">
            <span class="b">Item1</span>
            <span class="b">Item2</span>
            <span class="b">Item3</span>
            <span class="b">Item4</span>
         </div>
       </body>
    </html>"""

    expected_output_issue_93 = (
        """<?xml version="1.0" encoding="UTF-8" ?>\n<content>\n"""
        "<outer><inner>  Item1 </inner><inner>Item2 </inner><inner>Item3 </inner>"
        "<inner>Item4</inner></outer>\n</content>"
    )
    rules = {"div#class=a": ["outer"], "span#class=b": ["inner"]}

    inscriptis = Inscriptis(fromstring(html_issue_93), ParserConfig(annotation_rules=rules))
    annotated_html = {
        "text": inscriptis.get_text(),
        "label": inscriptis.get_annotations(),
    }
    result = XmlExtractor()(annotated_html)
    assert result == expected_output_issue_93


def test_tag_folding_issue_93_extended():
    html_issue_93 = """<html>
       <body>
         <div class="a">
         Some Test to add :)
            <span class="b">Item<b>1</b></span>
            <span class="b">Item2</span>
            <span class="b"><b>Item3</b></span>
            <span class="b"><b>It</b>e<b>m4</b></span>
         </div>
       </body>
    </html>"""

    expected_output_issue_93 = (
        """<?xml version="1.0" encoding="UTF-8" ?>\n"""
        """<content>\n"""
        """<outer>  Some Test to add :) <inner>Item <bold>1</bold></inner> <inner>Item2 </inner>"""
        """<inner><bold>Item3</bold></inner> <inner><bold>It</bold> e <bold>m4</bold></inner></outer>\n"""
        """</content>"""
    )
    rules = {"div#class=a": ["outer"], "span#class=b": ["inner"], "b": ["bold"]}

    inscriptis = Inscriptis(fromstring(html_issue_93), ParserConfig(annotation_rules=rules))
    annotated_html = {
        "text": inscriptis.get_text(),
        "label": inscriptis.get_annotations(),
    }
    result = XmlExtractor()(annotated_html)
    assert result == expected_output_issue_93

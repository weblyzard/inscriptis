#!/usr/bin/env python
# encoding: utf-8

"""
Tests the Table formatting with different parameters such as width and
alignment
"""

from inscriptis.annotation.parser import AnnotationModel, ApplyAnnotation
from inscriptis.model.html_element import HtmlElement


def test_parse():

    rules = {'table#border=1': ['table'],
             'hr': ['horizontal-line']}
    tags, attrs = AnnotationModel._parse(rules)

    assert tags == {'hr': ['horizontal-line']}

    apply_annotation= attrs[0]
    assert apply_annotation.match_tag == 'table'
    assert apply_annotation.match_value == '1'
    assert apply_annotation.attr == 'border'

    e = HtmlElement(tag='table')
    apply_annotation.apply('1', e)
    assert e.annotation == ('table', )


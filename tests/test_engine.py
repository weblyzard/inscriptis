# test borderline cases

from inscriptis import get_annotated_text, get_text


def test_text_from_empty_content():
    assert get_text("") == ""


def test_annotations_from_empty_content():
    assert get_annotated_text("") == {}

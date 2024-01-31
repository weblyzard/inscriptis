# test the annotation handling

import pytest

from inscriptis.annotation import Annotation
from inscriptis.html_engine import Inscriptis
from inscriptis.model.config import ParserConfig
from lxml.html import fromstring


def test_get_annotation():
    """Test get_anntation from the Inscriptis class"""
    html = "<b>Chur</b> is a City in <b>Switzerland</b>"
    rules = {'b': ['bold']}
    inscriptis = Inscriptis(fromstring(html), ParserConfig(annotation_rules=rules))

    # gettext needs to be called prior to get_annotations, since
    # otherwise no text to annotate is available.
    with pytest.raises(ValueError):
        annotation = inscriptis.get_annotations()

    # correct order
    text = inscriptis.get_text()
    annotations = inscriptis.get_annotations()

    assert text == "Chur is a City in Switzerland"
    assert annotations == [Annotation(start=0, end=4, metadata='bold'), Annotation(start=18, end=29, metadata='bold')]





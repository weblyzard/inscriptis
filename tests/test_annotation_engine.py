# test the annotation handling


from lxml.html import fromstring

from inscriptis.annotation import Annotation
from inscriptis.html_engine import Inscriptis
from inscriptis.model.config import ParserConfig


def test_get_annotation():
    """Test get_anntation from the Inscriptis class"""
    html = "<b>Chur</b> is a City in <b>Switzerland</b>"
    rules = {"b": ["bold"]}

    inscriptis = Inscriptis(fromstring(html), ParserConfig(annotation_rules=rules))

    assert inscriptis.get_text() == "Chur is a City in Switzerland"
    assert inscriptis.get_annotations() == [
        Annotation(start=0, end=4, metadata="bold"),
        Annotation(start=18, end=29, metadata="bold"),
    ]

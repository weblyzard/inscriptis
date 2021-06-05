"""
Parses annotation configuration files.

Annotation configuration files contain a dictionary that maps tags and
attributes to the corresponding annotation.

- tags are referenced by their name
- attributes by a # (e.g., #class) and an optional selector (e.g.,
  #class=short-description)

Example:
    {
        "h1": ["heading"],
        "b": ["emphasis"],
        "div#class=toc": ["table-of-contents"],
        "#class=short-description]": ["description"]
    }
"""
from inscriptis.model.html_element import HtmlElement

class ApplyAnnotation:
    """
    Applies an Annotation to the given attribute
    """
    def __init__(self, annotations: tuple, match_tag: str = None,
                 match_value: str = None):
        self.annotations = annotations
        if not match_tag and not match_value:
            self.apply = self.apply_all
        elif match_tag and match_value:
            self.apply = self.apply_matching
            self.matcher = lambda value, tag: self.tag == tag and \
                                              self.value in value.split()
        elif match_tag:
            self.apply = self.apply_matching
            self.matcher = lambda value, tag: self.tag == tag
        else:
            self.apply = self.apply_matching
            self.matcher = lambda value, tag: self.value in value.split()

    def apply_all(self, attr_value: str, html_element: HtmlElement):
        """
        Applies the annotations to HtmlElements.
        """
        html_element.annotations += self.annotations

    def apply_matching(self, attr_value: str, html_element: HtmlElement):
        """
        Applies the annotation to HtmlElements with matching tags.
        """
        if self.matcher(attr_value, html_element.tag):
            html_element.annotation += self.annotations


class AnnotationModel:

    def __init__(self, tags, attrs, values):
        self.tags = {}
        self.attrs = {}
        self.values = {}

    @staticmethod
    def parse(model: dict) -> 'AnnotationModel':
        """
        Parses a model dictionary and returns the corresponding
        AnnotationModel.

        Returns:
            the AnnotationModel matching the input dictionary.
        """
        for key, annotation in model.items():
            if '#' in key:
                pass

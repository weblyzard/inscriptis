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
from collections import defaultdict
from copy import copy

from inscriptis.model.html_element import HtmlElement, DEFAULT_HTML_ELEMENT


class ApplyAnnotation:
    """
    Applies an Annotation to the given attribute
    """

    __slots__ = ('annotations', 'match_tag', 'match_value', 'attr', 'apply',
                 'matcher')

    def __init__(self, annotations: tuple, attr: str, match_tag: str = None,
                 match_value: str = None):
        self.attr = attr
        self.annotations = tuple(annotations)
        self.match_tag = match_tag
        self.match_value = match_value

        if not match_tag and not match_value:
            self.apply = self.apply_all
        elif match_tag and match_value:
            self.apply = self.apply_matching
            self.matcher = lambda value, tag: self.match_tag == tag and \
                                              self.match_value in value.split()
        elif match_tag:
            self.apply = self.apply_matching
            self.matcher = lambda value, tag: self.match_tag == tag
        else:
            self.apply = self.apply_matching
            self.matcher = lambda value, tag: self.match_value in value.split()

    def apply_all(self, _: str, html_element: HtmlElement):
        """
        Applies the annotations to HtmlElements.
        """
        html_element.annotation += self.annotations

    def apply_matching(self, attr_value: str, html_element: HtmlElement):
        """
        Applies the annotation to HtmlElements with matching tags.
        """
        print(attr_value, self.match_value, ">", html_element.tag, self.match_tag)
        if self.matcher(attr_value, html_element.tag):
            html_element.annotation += self.annotations


class AnnotationModel:

    def __init__(self, css_profile, model: dict):
        tags, self.css_attr = self._parse(model)
        for tag, annotations in tags.items():
            if tag not in css_profile:
                css_profile[tag] = copy(DEFAULT_HTML_ELEMENT)
            css_profile[tag].annotation += tuple(annotations)
        self.css = css_profile

    @staticmethod
    def _parse(model: dict) -> 'AnnotationModel':
        """
        Parses a model dictionary and returns the corresponding
        AnnotationModel.

        Returns:
            the AnnotationModel matching the input dictionary.
        """
        tags = defaultdict(list)
        attrs = []
        for key, annotations in model.items():
            if '#' in key:
                tag, attr = key.split('#')
                if '=' in attr:
                    attr, value = attr.split('=')
                else:
                    value = None
                attrs.append(ApplyAnnotation(annotations, attr,
                                             tag, value))
            else:
                tags[key].extend(annotations)
        return tags, attrs

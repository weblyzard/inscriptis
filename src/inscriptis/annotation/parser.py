"""Parse annotation configuration files.

Annotation configuration files contain a dictionary that maps tags and
attributes to the corresponding annotation.

  - tags are referenced by their name
  - attributes by a `#` (e.g., `#class`) and an optional selector (e.g.,
    `#class=short-description`)

Example::

    {
        "h1": ["heading"],
        "b": ["emphasis"],
        "div#class=toc": ["table-of-contents"],
        "#class=short-description]": ["description"]
    }
"""

from collections import defaultdict
from copy import copy

from inscriptis.model.html_element import DEFAULT_HTML_ELEMENT, HtmlElement


class ApplyAnnotation:
    """Apply an Annotation to the given attribute.

    Arguments:
        annotations: a tuple of annotations to be applied to the attribute.
        attr: the name of the attribute.
        match_tag: only apply annotations to attributes that belong to the
                   given match_tag.
        match_value: only apply annotations to attribute with the given
                     match_value.

    """

    __slots__ = ("annotations", "attr", "match_tag", "match_value", "matcher")

    def __init__(
        self,
        annotations: tuple,
        attr: str,
        match_tag: str = "",
        match_value: str = "",
    ):
        self.annotations = tuple(annotations)
        self.attr = attr
        self.match_tag = match_tag
        self.match_value = match_value

    def apply(self, attr_value: str, html_element: HtmlElement):
        """Apply the annotation to HtmlElements with matching tags."""
        if (self.match_tag and self.match_tag != html_element.tag) or (
            self.match_value and self.match_value not in attr_value.split()
        ):
            return

        html_element.annotation += self.annotations

    def __str__(self):
        return "<ApplyAnnotation: {tag}#{attr}={value}".format(
            tag=self.match_tag or "{any}",
            attr=self.attr or "{any}",
            value=self.match_value or "{any}",
        )

    __repr__ = __str__


class AnnotationModel:
    """Adapt the CSS profile and CSS attributes for annotation support.

    Attributes:
        css: the refined CSS class which contains annotations for HtmlElements
             which should be annotated.
        css_attr: information on CSS attributes that shall be annotated.

    """

    def __init__(self, css_profile, model: dict):
        tags, self.css_attr = self._parse(model)
        for tag, annotations in tags.items():
            if tag not in css_profile:
                css_profile[tag] = copy(DEFAULT_HTML_ELEMENT)
            css_profile[tag].annotation += tuple(annotations)
        self.css = css_profile

    @staticmethod
    def _parse(model: dict) -> tuple[dict, list]:
        """Compute the AnnotationModel from a model dictionary.

        Returns:
            the AnnotationModel matching the input dictionary.

        """
        tags = defaultdict(list)
        attrs = []
        for key, annotations in model.items():
            if "#" in key:
                tag, attr = key.split("#")
                if "=" in attr:
                    attr, value = attr.split("=")
                else:
                    value = None
                attrs.append(ApplyAnnotation(annotations, attr, tag, value))
            else:
                tags[key].extend(annotations)
        return tags, attrs

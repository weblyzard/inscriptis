#!/usr/bin/env python
"""Provide configuration objects for the Inscriptis HTML to text converter."""

from copy import deepcopy

from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.annotation.parser import AnnotationModel
from inscriptis.model.attribute import Attribute

DEFAULT_CSS_PROFILE_NAME = 'relaxed'


class ParserConfig:
    """Encapsulate configuration options and CSS definitions."""

    def __init__(self, css=None, display_images=False,
                 deduplicate_captions=False, display_links=False,
                 display_anchors=False, annotation_rules=None):
        """Create a ParserConfig configuration.

        Args:
            css: an optional custom CSS definition.
            display_images: whether to include image tiles/alt texts.
            deduplicate_captions: whether to deduplicate captions such as image
                titles (many newspaper include images and video previews with
                identical titles).
            display_links: whether to display link targets
                           (e.g. `[Python](https://www.python.org)`).
            display_anchors: whether to display anchors (e.g. `[here](#here)`).
            annotation_rules: an optional dictionary of annotation rules which
                              specify tags and attributes to annotation.
        """
        self.display_images = display_images
        self.deduplicate_captions = deduplicate_captions
        self.display_links = display_links
        self.display_anchors = display_anchors
        self.css = css or CSS_PROFILES[DEFAULT_CSS_PROFILE_NAME]
        self.attribute_handler = Attribute()
        if annotation_rules:
            # ensure that we do not modify the original model or its
            # members.
            annotation_model = AnnotationModel(deepcopy(self.css),
                                               annotation_rules)
            # css with annotation support
            self.css = annotation_model.css
            # attribute handler with annotation support
            self.attribute_handler.merge_attribute_map(
                annotation_model.css_attr)

    def parse_a(self) -> bool:
        """Indicate whether the text output should contain links or anchors.

        Returns
            Whether we need to parse <a> tags.
        """
        return self.display_links or self.display_anchors

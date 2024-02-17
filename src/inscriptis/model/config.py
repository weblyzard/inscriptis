#!/usr/bin/env python
"""Provide configuration objects for the Inscriptis HTML to text converter."""
from __future__ import annotations

from copy import deepcopy
from typing import Dict, List

from inscriptis.annotation.parser import AnnotationModel
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.attribute import Attribute
from inscriptis.model.html_element import HtmlElement
from inscriptis.model.tag import CustomHtmlTagHandlerMapping

DEFAULT_CSS_PROFILE_NAME = "relaxed"


class ParserConfig:
    """Encapsulate configuration options and CSS definitions."""

    def __init__(
        self,
        css: Dict[str, HtmlElement] = None,
        display_images: bool = False,
        deduplicate_captions: bool = False,
        display_links: bool = False,
        display_anchors: bool = False,
        annotation_rules: Dict[str, List[str]] = None,
        table_cell_separator: str = "  ",
        custom_html_tag_handler_mapping: CustomHtmlTagHandlerMapping = None,
    ):
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
            table_cell_separator: separator to use between table cells.
            custom_html_tag_handler_mapping: an optional CustomHtmlTagHandler
        """
        self.display_images = display_images
        self.deduplicate_captions = deduplicate_captions
        self.display_links = display_links
        self.display_anchors = display_anchors
        self.css = css or CSS_PROFILES[DEFAULT_CSS_PROFILE_NAME]
        self.attribute_handler = Attribute()
        self.table_cell_separator = table_cell_separator
        self.custom_html_tag_handler_mapping = custom_html_tag_handler_mapping

        if annotation_rules:
            # ensure that we do not modify the original model or its
            # members.
            annotation_model = AnnotationModel(deepcopy(self.css), annotation_rules)
            # css with annotation support
            self.css = annotation_model.css
            # attribute handler with annotation support
            self.attribute_handler.merge_attribute_map(annotation_model.css_attr)

    def parse_a(self) -> bool:
        """Indicate whether the text output should contain links or anchors.

        Returns
            Whether we need to parse <a> tags.
        """
        return self.display_links or self.display_anchors

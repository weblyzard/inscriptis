#!/usr/bin/env python
"""Configure Inscripits HTML rendering."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

from inscriptis.annotation.parser import AnnotationModel
from inscriptis.css_profiles import CSS_PROFILES
from inscriptis.model.attribute import Attribute

DEFAULT_CSS_PROFILE_NAME = "relaxed"

if TYPE_CHECKING:
    from inscriptis.model.html_element import HtmlElement
    from inscriptis.model.tag import CustomHtmlTagHandlerMapping


class ParserConfig:
    """The ParserConfig class allows fine-tuning the HTML rendering.

    - CSS definitions (from :mod:`inscriptis.css_profiles` or custom
      definitions).
    - configuration options for handling images, captions, links, etc.
    - annotation rules, if Inscripitis is used for annotating text.
    - custom html tag handlers.

    Attributes:
            css: An optional custom CSS definition.
            display_images: Whether to include image tiles/alt texts.
            deduplicate_captions: Whether to deduplicate captions such as image
                titles (many newspaper include images and video previews with
                identical titles).
            display_links: Whether to display link targets
                           (e.g. `[Python](https://www.python.org)`).
            display_anchors: Whether to display anchors (e.g. `[here](#here)`).
            annotation_rules: An optional dictionary of annotation rules which
                              specify tags and attributes to annotation.
            table_cell_separator: Separator to use between table cells.
            custom_html_tag_handler_mapping: An optional CustomHtmlTagHandler.


    The following example demonstrates how ParserConfig is used to

    - enable the strict CSS profile and
    - prevent links from being shown.

    .. code-block:: Python

       from inscriptis import get_text
       from inscriptis.css_profiles import CSS_PROFILES
       from inscriptis.model.config import ParserConfig

       css_profile = CSS_PROFILES['strict'].copy()
       config = ParserConfig(css=css_profile, display_links=False)
       text = get_text('fi<span>r</span>st <a href="/first">link</a>', config)
       print(text)

    """

    def __init__(
        self,
        css: dict[str, HtmlElement] | None = None,
        display_images: bool = False,
        deduplicate_captions: bool = False,
        display_links: bool = False,
        display_anchors: bool = False,
        annotation_rules: dict[str, list[str]] | None = None,
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

        Returns:
            Whether we need to parse <a> tags.

        """
        return self.display_links or self.display_anchors

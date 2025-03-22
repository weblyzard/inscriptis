"""HTML Annotation Processor."""

from collections import defaultdict
from itertools import cycle
from typing import Dict, Any, List

from inscriptis.annotation import Annotation
from inscriptis.annotation.output import AnnotationProcessor

COLOR_SCHEMA = ("#D8115980", "#8F2D5680", "#21838080", "#FBB13C80", "#73D2DE80")


class HtmlExtractor(AnnotationProcessor):
    """Provides an HTML version of the extracted text.

    The generated HTML colors annotations based on the COLOR_SCHEMA
    constant.
    """

    verbatim = True

    def __call__(self, annotated_text: Dict[str, Any]) -> str:
        tag_dict = defaultdict(list)
        for start, end, label in sorted(
            Annotation(s, e, t) for s, e, t in reversed(annotated_text["label"])
        ):
            tag_dict[start].append(f'<span class="{label}" data-label="{label}">')
            tag_dict[end].insert(0, f"</span>")

        tagged_content = [
            "<html><head><style>",
            self._get_css(annotated_text["label"]),
            "</style></head><body><pre>",
        ]

        text = annotated_text["text"]
        current_idx = 0
        for idx, tags in sorted(tag_dict.items()):
            tagged_content.append(text[current_idx:idx])
            current_idx = idx
            tagged_content.extend(tags)
        tagged_content.append(text[current_idx:])
        return "".join(tagged_content) + "</pre></body></html>"

    @staticmethod
    def _get_label_colors(labels: List[str]) -> Dict[str, str]:
        """Compute the mapping between annotation labels and colors.

        The used color schema is available in the global variable COLOR_SCHEMA.

        Args:
            labels: a list of the annotations classes (e.g., heading, etc.)
                    that need to be color-coded.
        Returns:
            A mapping between the available labels and the corresponding color
            from the COLOR_SCHEMA.
        """
        return dict(zip({a[2] for a in sorted(labels)}, cycle(COLOR_SCHEMA)))

    def _get_css(self, labels: List[str]) -> str:
        """Compute the CSS to be included into the HTML output.

        Args:
            labels: a list of the annotations classes (e.g., heading, etc.)
                    that need to be color-coded.

        Returns:
            A string containing the CSS to be embedded into the HTML output.

        """
        css = []
        for label, color in sorted(self._get_label_colors(labels).items()):
            css.append(
                "pre{{"
                "position: relative; white-space: pre; line-height: 2.5; font-family: monospace;"
                "}}\n"
                ".{label} {{ position: relative; display: inline-block; white-space: pre;"
                "  background-color: {color}; \n"
                "  border-radius: 0.4em; padding: 0 4px\n"
                "}}\n"
                ".{label}::before {{"
                "content: attr(data-label); position: absolute; top: -1.3em; left: 0;"
                "background-color: {color}; "
                "font-size: 65%; padding: 0px 2px; border-radius: 1px; white-space: nowrap; font-weight: bold;"
                " }}\n".format(label=label, color=color)
            )
        return "\n".join(css)

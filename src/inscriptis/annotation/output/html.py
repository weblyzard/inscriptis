"""HTML Annotation Processor."""
from collections import defaultdict
from itertools import cycle
from typing import Dict, Any, List

from inscriptis.annotation.output import AnnotationProcessor

COLOR_SCHEMA = ('#D8115980', '#8F2D5680', '#21838080',
                '#FBB13C80', '#73D2DE80')


class HtmlExtractor(AnnotationProcessor):
    """Provides an HTML version of the extracted text.

    The generated HTML colors annotations based on the COLOR_SCHEMA
    constant.
    """

    verbatim = True

    def __call__(self, annotated_text: Dict[str, Any]) -> str:
        tag_indices = defaultdict(list)

        for start, end, label in sorted(annotated_text['label']):
            tag_indices[start].append(label)
            tag_indices[end].append('/' + label)

        open_tags = []
        tagged_content = ['<html><head><style>',
                          self._get_css(annotated_text['label']),
                          '</style></head><body><pre>']
        for idx, ch in enumerate(annotated_text['text']):
            if idx in tag_indices:
                tags = tag_indices[idx]
                # close tags:
                for _ in (t for t in sorted(tags, reverse=True)
                          if t.startswith('/')):
                    open_tags.pop()
                    tagged_content.append('</span>')
                # open tags
                for tag in (t for t in sorted(tags, reverse=True)
                            if not t.startswith('/')):
                    open_tags.append(tag)
                    tagged_content.append(
                        '<span class="{tag}-label">{tag}</span>'
                        '<span class="{tag}">'.format(tag=tag))

            if ch == '\n':
                tagged_content.extend(['</span>' for _ in open_tags])
                tagged_content.append('</pre>\n<pre>')
                tagged_content.extend(['<span class="{tag}">'.format(tag=tag)
                                       for tag in open_tags])
            else:
                tagged_content.append(ch)

        return ''.join(tagged_content) + '</pre></body></html>'

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
        return {label: color
                for label, color in zip({a[2] for a in sorted(labels)},
                                        cycle(COLOR_SCHEMA))}

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
                'pre{{'
                '  position: relative;\n'
                '}}\n'
                '.{label} {{\n'
                '  background-color: {color};\n'
                '  border-radius: 0.4em;\n'
                '}}\n'
                '.{label}-label {{\n'
                '  top: -1.0em;\n'
                '  content: "{label}";\n'
                '  position: absolute;\n'
                '  background-color: {color};\n'
                '  font-size: 75%; }}\n'.format(label=label,
                                                color=color))
        return '\n'.join(css)

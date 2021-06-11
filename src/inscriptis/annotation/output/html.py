from collections import defaultdict
from itertools import cycle
from typing import Dict, Any

from inscriptis.annotation.output import AnnotationProcessor

COLOR_SCHEMA = ('#D81159', '#8F2D56', '#218380', '#FBB13C', '#73D2DE')
COLOR_SCHEMA = ('#D8115980', '#8F2D5680', '#21838080',
                '#FBB13C80', '#73D2DE80')


class HtmlExtractor(AnnotationProcessor):

    verbatim = True

    """
    Provides an HTML version of the extracted text with colored annotations.
    """
    def __call__(self, annotated_text: Dict[str, Any]) -> Dict[str, Any]:
        tag_indices = defaultdict(list)

        for start, end, label in sorted(annotated_text['label']):
            tag_indices[start].append(label)
            tag_indices[end].append('/' + label)

        current_idx = 0
        tagged_content = ['<html><head><style>',
                          self._get_css(annotated_text['label']),
                          '</style><body><pre>']
        text = annotated_text['text']
        for index, tags in sorted(tag_indices.items()):
            tagged_content.append(text[current_idx:index])
            # close tags
            tagged_content.extend(['</span>'
                                   for tag in sorted(tags, reverse=True)
                                   if tag.startswith('/')])
            # open tags
            tagged_content.extend(['<span class="{tag}">'.format(tag=tag)
                                   for tag in sorted(tags)
                                   if not tag.startswith('/')])
            current_idx = index
        tagged_content.append(text[current_idx:])
        tagged_content.append("</pre></body></html>")

        return ''.join(tagged_content)

    @staticmethod
    def _get_label_colors(labels) -> Dict[str, str]:
        """

        Returns:
            A mapping between the available labels and the corresponding color
            from the COLOR_SCHEMA.
        """
        return {label: color for label, color in zip({a[2] for a in labels},
                                                     cycle(COLOR_SCHEMA))}

    def _get_css(self, labels) -> str:
        css = []
        for label, color in sorted(self._get_label_colors(labels).items()):
            css.append('.{label} {{\n'
                       '  background-color: {color};\n'
                       '}}\n'
                       '.{label}:before {{\n'
                       '  top: -1.0em;\n'
                       '  content: "{label}";\n'
                       '  position: relative;\n'
                       '  background-color: {color};\n'
                       '  font-size: 75%; }}\n'.format(label=label,
                                                       color=color))
        return '\n'.join(css)
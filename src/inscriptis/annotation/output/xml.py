"""XML Annotation processor."""
from collections import defaultdict
from typing import Dict, Any

from inscriptis.annotation.output import AnnotationProcessor


class XmlExtractor(AnnotationProcessor):
    """Provide the converted text with XML-style annotations."""

    verbatim = True

    def __call__(self, annotated_text: Dict[str, Any]) -> str:
        """Provide an XML version of the given text and annotations.

        Args:
            annotated_text: a dictionary containing the plain text and the
                            extracted annotations.

        Returns:
            A string with the XML-version of the content.
        """
        tag_indices = defaultdict(list)

        for start, end, label in sorted(annotated_text['label']):
            tag_indices[start].append(label)
            tag_indices[end].append('/' + label)

        current_idx = 0
        tagged_content = ['<?xml version="1.0" encoding="UTF-8" ?>\n']
        text = annotated_text['text']
        for index, tags in sorted(tag_indices.items()):
            tagged_content.append(text[current_idx:index])
            # close tags
            tagged_content.extend(['<' + tag + '>'
                                   for tag in sorted(tags, reverse=True)
                                   if tag.startswith('/')])
            # open tags
            tagged_content.extend(['<' + tag + '>' for tag in sorted(tags)
                                   if not tag.startswith('/')])
            current_idx = index
        tagged_content.append(text[current_idx:])

        return ''.join(tagged_content)

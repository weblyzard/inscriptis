"""XML Annotation processor."""

from collections import defaultdict
from typing import Any

from inscriptis.annotation.output import AnnotationProcessor


class XmlExtractor(AnnotationProcessor):
    """Provide the converted text with XML-style annotations."""

    verbatim = True

    def __call__(self, annotated_text: dict[str, Any], root_element="content"):
        tag_dict = defaultdict(list)
        for start, end, tag in reversed(annotated_text["label"]):
            tag_dict[start].append(f"<{tag}>")
            tag_dict[end].insert(0, f"</{tag}>")

        current_idx = 0
        text = annotated_text["text"]
        tagged_content = ['<?xml version="1.0" encoding="UTF-8" ?>\n', "<content>\n"]
        for idx, tags in sorted(tag_dict.items()):
            tagged_content.append(text[current_idx:idx])
            current_idx = idx
            tagged_content.extend(tags)

        tagged_content.append(text[current_idx:])
        tagged_content.append("\n</content>")
        return "".join(tagged_content)

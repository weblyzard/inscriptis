"""XML Annotation processor."""
from collections import defaultdict
from typing import Dict, Any, Tuple

from lxml import etree
from inscriptis.annotation.output import AnnotationProcessor


class XmlExtractor(AnnotationProcessor):
    """Provide the converted text with XML-style annotations."""

    verbatim = True

    def traverse_element(self, root, text, start, end, annotations, idx) -> int:
        while idx + 1 < len(annotations):
            idx += 1
            next_start, next_end, label = annotations[idx]["label"]
            # recurse?
            if next_start < end:
                leaf = etree.Element(root, label)
                cascaded_end = self.traverse_element(leaf, text, next_start, next_end, idx)
            else:
                root.tail += text[start: cascaded_end]



    def __call__(self, annotated_text: Dict[str, Any], root_element='r') -> str:
        text = annotated_text["text"]
        annotations = sorted(annotated_text["label"])
        root = etree.Element(root_element)
        current_annotation_idx = 0
        while current_annotation_idx < len(annotations):
            current_annotation_idx = self.traverse_element(root, text, annotations, idx)


        for start, end, label in sorted(annotated_text["label"]):
            current_element = etree.SubElement(root, label)
            current_element.text = text[start:end]

        return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    def call3(self, annotated_text: Dict[str, Any]) -> str:
        tag_indices = defaultdict(list)

        for start, end, label in sorted(annotated_text["label"]):
            length = end - start
            tag_indices[start].append((label, length))
            tag_indices[end].append(("/" + label, length))

        current_idx = 0
        tagged_content = ['<?xml version="1.0" encoding="UTF-8" ?>\n']
        text = annotated_text["text"]
        for index, tags in sorted(tag_indices.items()):
            tagged_content.append(text[current_idx:index])

            # Separate closing vs opening tags
            closing_tags = [t for t in tags if t[0].startswith("/")]
            opening_tags = [t for t in tags if not t[0].startswith("/")]

            # Sort closing tags by ascending length (so outer closes last)
            closing_tags.sort(key=lambda x: x[1])
            for tag, _ in closing_tags:
                tagged_content.append(f"<{tag}>")

            # Sort opening tags by descending length (so outer opens first)
            opening_tags.sort(key=lambda x: x[1], reverse=True)
            for tag, _ in opening_tags:
                tagged_content.append(f"<{tag}>")

            current_idx = index
        tagged_content.append(text[current_idx:])

        return "".join(tagged_content)

    def call2(self, annotated_text: Dict[str, Any]) -> str:
        """Provide an XML version of the given text and annotations.

        Args:
            annotated_text: a dictionary containing the plain text and the
                            extracted annotations.

        Returns:
            A string with the XML-version of the content.
        """
        tag_indices = defaultdict(list)

        for start, end, label in sorted(annotated_text["label"]):
            tag_indices[start].append(label)
            tag_indices[end].append("/" + label)

        current_idx = 0
        tagged_content = ['<?xml version="1.0" encoding="UTF-8" ?>\n']
        text = annotated_text["text"]
        for index, tags in sorted(tag_indices.items()):
            tagged_content.append(text[current_idx:index])
            # close tags
            tagged_content.extend(
                [
                    "<" + tag + ">"
                    for tag in sorted(tags, reverse=True)
                    if tag.startswith("/")
                ]
            )
            # open tags
            tagged_content.extend(
                ["<" + tag + ">" for tag in sorted(tags) if not tag.startswith("/")]
            )
            current_idx = index
        tagged_content.append(text[current_idx:])

        return "".join(tagged_content)

from collections import defaultdict
from typing import Dict, Any

from inscriptis.annotation.output import AnnotationProcessor


class TagExtractor(AnnotationProcessor):
    """
    Provides an annotated version of the text output using XML-style tags.
    """
    def __call__(self, annotated_text: Dict[str, Any]) -> Dict[str, Any]:
        tag_indices = defaultdict(list)

        for start, end, label in annotated_text['label']:
            tag_indices[start].append(label)
            tag_indices[end].append('/' + label)

        current_idx = 0
        tagged_content = []
        text = annotated_text['text']
        for index, tags in tag_indices.items():
            tagged_content.append(text[current_idx:index])
            # close tags
            tagged_content.extend(['<' + tag + '>' for tag in reversed(tags)
                                   if tag.startswith('/')])
            # open tags
            tagged_content.extend(['<' + tag + '>' for tag in tags
                                   if not tag.startswith('/')])
            current_idx = index
        tagged_content.append(text[current_idx:])

        annotated_text['tag'] = ''.join(tagged_content)
        return annotated_text

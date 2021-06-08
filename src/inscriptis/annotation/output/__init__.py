"""
Interface for customizing the annotation output provided by Inscriptis.
"""
from typing import Dict


class AnnotationFormatter:

    def __call__(self, annotated_text: Dict[str, str]) -> Dict[str, str]:
        raise NotImplemented

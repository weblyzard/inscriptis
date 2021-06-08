from typing import Dict, Any

from inscriptis.annotation.output import AnnotationProcessor


class SurfaceExtractor(AnnotationProcessor):
    """
    Extracts the surface form of all annotated labels.
    """
    def __call__(self, annotated_text: Dict[str, Any]) -> Dict[str, Any]:
        surface_forms = [(label, annotated_text['text'][start:end])
                         for start, end, label in annotated_text['label']]
        annotated_text['surface_form'] = surface_forms
        return annotated_text

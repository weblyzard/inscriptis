"""Surface Form Annotation Processor."""
from typing import Dict, Any

from inscriptis.annotation.output import AnnotationProcessor


class SurfaceExtractor(AnnotationProcessor):
    """Extracts the surface form of all annotated labels."""

    verbatim = False

    def __call__(self, annotated_text: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add information on the surface forms to the annotated_text dictionary.

        Args:
            annotated_text: a dictionary containing the plain text and the
                            extracted annotations.

        Returns:
            An extended dictionary which contains the extracted surface-forms
            of the annotations under the key 'surface'.
        """
        surface_forms = [
            (label, annotated_text["text"][start:end])
            for start, end, label in annotated_text["label"]
        ]
        annotated_text["surface"] = surface_forms
        return annotated_text

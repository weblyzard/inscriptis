"""Interface for customizing the annotation output provided by Inscriptis."""
from typing import Dict, Any


class AnnotationProcessor:
    """An AnnotationProcessor is called for formatting annotations."""

    def __call__(self, annotated_text: Dict[str, str]) -> Any:
        """Format the given text and annotations.

        Args:
            annotated_text: a dictionary that contains the converted text and
                            all annotations that have been found.

        Returns:
            An output representation that has been changed according to the
            AnnotationProcessor's design.
        """
        raise NotImplementedError

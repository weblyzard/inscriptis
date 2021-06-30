r""":class:`AnnotationProcessor`\s transform annotations to an output format.

All AnnotationProcessor's implement the :class:`AnnotationProcessor` interface
by overwrite the class's :meth:`AnnotationProcessor.__call__` method.

.. note::
    1. The AnnotationExtractor class must be put into a package with the
       extractor's name (e.g., :mod:`inscriptis.annotation.output.*package*`)
       and be named :class:`*PackageExtractor*` (see the examples below).
    2. The overwritten :meth:`__call__` method may either extend the original
       dictionary which contains the extracted text and annotations (e.g.,
       :class:`~inscriptis.annotation.output.surface.SurfaceExtractor`) or
       may replace it with an custom output (e.g.,
       :class:`~inscriptis.annotation.output.html.HtmlExtractor` and
       :class:`~inscriptis.annotation.output.xml.XmlExtractor`.

Currently, Inscriptis supports the following built-in AnnotationProcessors:

 1. :class:`~inscriptis.annotation.output.html.HtmlExtractor` provides an
    annotated HTML output format.
 2. :class:`~inscriptis.annotation.output.xml.XmlExtractor` yields an output
    which marks annotations with XML tags.
 3. :class:`~inscriptis.annotation.output.surface.SurfaceExtractor` adds the
    key `surface` to the result dictionary which contains the surface forms
    of the extracted annotations.

"""
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

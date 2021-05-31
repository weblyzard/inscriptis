"""
The model used for saving annotations.
"""

from collections import namedtuple

Annotation = namedtuple('Annotation', 'start end text metadata')

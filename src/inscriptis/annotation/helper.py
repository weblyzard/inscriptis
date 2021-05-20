"""
This module contains classes used for annotating the extracted text content.
"""

from abc import ABC, abstractmethod


class AbstractAnnotationHelper(ABC):

    @abstractmethod
    def add_table(self, text):
        pass

    @abstractmethod
    def add_table_cell(self, text):
        pass


class AnnotationHelper(AbstractAnnotationHelper):

    def __init__(self):
        self.annotations = []
        self.current_pos = 0

    def add_text(self, text):
        """
        Register the following text which has been added to the result.

        Args:
            text: the text which has been added to the result.

        """
        self.current_pos += len(text)

    def add_table(self, text):
        pass

    def add_table_cell(self, text):
        pass

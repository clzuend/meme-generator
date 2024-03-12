"""Implements the IngestorInterface."""
from abc import ABC, abstractmethod
from typing import List
from os.path import splitext

from .QuoteModel import QuoteModel


class IngestorInterface(ABC):
    """
    An abstract class representing the Ingestor strategy.

    Attributes:
        allowed_extensions : List -- allowed extensions (overwritten)

    Methods:
        can_ingest(path) -- Test if document can be ingested.
        parse(path) -- Parse the document and ingest to QuoteModel.
    """

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Test if document can be ingested.

        Parameters:
            path : str -- the path of the document
        """
        _, ext = splitext(path)
        return ext in cls.allowed_extensions

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the document and ingest to QuoteModel.

        Parameters:
            path : str -- the path of the document
        """
        if not cls.can_ingest(path):
            raise Exception('Cannot ingest document.')

        try:
            quotes = cls.parse_special(path)
        except Exception:
            print('Something went wrong. Some quotes have not been ingested.')
            quotes = cls.parse_special(path)

        return quotes

    @classmethod
    @abstractmethod
    def parse_special(cls, path: str) -> List[QuoteModel]:
        """
        Parse specific document type and ingest to QuoteModel.

        Parameters:
            path : str -- the path of the document
        """
        pass

"""Implements the Ingestor."""
from typing import List

from .QuoteModel import QuoteModel
from .IngestorInterface import IngestorInterface
from .TextIngestor import TextIngestor
from .DocxIngestor import DocxIngestor
from .PDFIngestor import PDFIngestor
from .CSVIngestor import CSVIngestor

class Ingestor(IngestorInterface):
    """
    A class representing the Ingestor strategy to pick an Ingestor based on the document type.
    
    Attributes:
        ingestors : List -- allowed ingestors
        
    Methods:
        parse(path) -- Parse the document and ingest to QuoteModel.
    """

    ingestors = [TextIngestor, DocxIngestor, PDFIngestor, CSVIngestor]
    
    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Loop over ingestors and ingest to QuoteModel.
        
        Parameters:
            path : str -- the path of the document
        """
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise Exception('No suitable ingestor.')
                
    
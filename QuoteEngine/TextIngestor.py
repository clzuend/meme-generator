"""
Implements the TextIngestor.
"""

from typing import List

from .QuoteModel import QuoteModel
from .IngestorInterface import IngestorInterface

class TextIngestor(IngestorInterface):
    """
    A class representing the Ingestor strategy for .txt files.
    
    Attributes:
        allowed_extensions : ['.txt'] (overwrites parent class)
        
    Methods:
        can_ingest(path) -- Test if document can be ingested.
        parse(parse) -- Parse the document and ingest to QuoteModel.
    """
    
    allowed_extensions = ['.txt']
    
    @classmethod
    def parse_special(cls, path:str) -> List[QuoteModel]:
        """
        Parse .txt file and ingest to QuoteModel.
        
        Parameters:
            path : str -- the path of the document
        """
        quotes = []
        
        with open(path) as f:
            for line in f:
                if line.count('-')==1:
                    body, author = line.split('-')
                    quote = QuoteModel(body.strip(), author.strip())
                    quotes.append(quote)

        return quotes
    
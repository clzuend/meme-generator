"""
Implements the DocxIngestor.
"""
import docx
from typing import List

from .QuoteModel import QuoteModel
from .IngestorInterface import IngestorInterface

class DocxIngestor(IngestorInterface):
    """
    A class representing the Ingestor strategy for .docx files.
    
    Attributes:
        allowed_extensions : ['.docx'] (overwrites parent class)
        
    Methods:
        can_ingest(path) -- Test if document can be ingested.
        parse(parse) -- Parse the document and ingest to QuoteModel.
    """
    
    allowed_extensions = ['.docx']
    
    @classmethod
    def parse_special(cls, path:str) -> List[QuoteModel]:
        """
        Parse .docx file and ingest to QuoteModel.
        
        Parameters:
            path : str -- the path of the document
        """
        quotes = []
        
        doc = docx.Document(path)
        
        for para in doc.paragraphs:
            if para.text.count('-')==1:
                body, author = para.text.split('-')
                quote = QuoteModel(body.strip(), author.strip())
                quotes.append(quote)

        return quotes
    
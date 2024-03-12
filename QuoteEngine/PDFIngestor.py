"""
Implements the PDFIngestor.
"""
import os
import subprocess
from typing import List
from random import randint

from .QuoteModel import QuoteModel
from .IngestorInterface import IngestorInterface

class PDFIngestor(IngestorInterface):
    """
    A class representing the Ingestor strategy for .pdf files.
    
    Attributes:
        allowed_extensions : ['.pdf'] (overwrites parent class)
        
    Methods:
        can_ingest(path) -- Test if document can be ingested.
        parse(parse) -- Parse the document and ingest to QuoteModel.
    """
    
    allowed_extensions = ['.pdf']
    
    @classmethod
    def parse_special(cls, path:str) -> List[QuoteModel]:
        """
        Parse .pdf file and ingest to QuoteModel.
        
        Parameters:
            path : str -- the path of the document
        """
        quotes = []
        
        tmp = f'./tmp/{randint(0,100000000)}.txt'
        call = subprocess.call(['pdftotext', path, tmp])
        with open(tmp, "r") as f:
            for line in f:
                line = line.strip('\n\r').strip()
                if line.count('-')==1:
                    body, author = line.split('-')
                    quote = QuoteModel(body.strip(), author.strip())
                    quotes.append(quote)
        os.remove(tmp)

        return quotes

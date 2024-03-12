import pandas as pd
from typing import List

from .QuoteModel import QuoteModel
from .IngestorInterface import IngestorInterface

class CSVIngestor(IngestorInterface):
    """
    A class representing the Ingestor strategy for .csv files.
    
    Attributes:
        allowed_extensions : ['.csv'] (overwrites parent class)
        
    Methods:
        can_ingest(path) -- Test if document can be ingested.
        parse(parse) -- Parse the document and ingest to QuoteModel.
    """
    allowed_extensions = ['.csv']
    
    @classmethod
    def parse_special(cls, path:str) -> List[QuoteModel]:
        """
        Parse .csv file and ingest to QuoteModel.
        
        Parameters:
            path : str -- the path of the document
        """
        quotes = []
        
        df = pd.read_csv(path, header=0)
        for _, row in df.iterrows():
            quote = QuoteModel(row['body'], row['author'])
            quotes.append(quote)

        return quotes
    
"""
Implements the QuoteModel.
"""
class QuoteModel():
    """
    A class to represent quotes.
    
    Attributes:
        body : str -- text body of the quote
        author : str -- author of the quote
    """

    def __init__(self, body:str, author:str):
        """Create a new quote."""
        self.body = body.strip('"')
        self.author = author
        
    def __str__(self) -> None:
        """Format string representation for QuoteModel instance."""
        return f'"{self.body}" - {self.author}'
    
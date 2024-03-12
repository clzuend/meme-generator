"""Implements the MemeEngine."""
import os
import imagehash
from typing import Tuple
from random import randint
from PIL import Image, ImageDraw, ImageFont

class MemeEngine():
    """
    A class to represent the MemeEngine.
    
    Main attributes:
        base_path: str -- Base path to save memes
        fnt_path: str -- Path to font
        fnt_size: str -- Maximum font size for quote (might get scaled smaller)
        max_words: str -- Maximum number of words per line for quote
        padding: str -- Padding between text and image boarder as a fraction
        gap: str -- Gap between quote body and author in pixels
    
    
    Main methods:
        make_meme(img_path, text, author, width=500) -- Create meme from image, text and author.
    """
    
    def __init__(self, base_path: str='./static', 
                 fnt_path: str='./fonts/LilitaOne-Regular.ttf', fnt_size: int=40,
                 max_words: int=6, padding: float=0.05, gap: int=10):
        """
        Initialize a new MemeEngine.
        
        Arguments:
            base_path: str -- Base path to save memes
            fnt_path: str -- Path to font
            fnt_size: str -- Maximum font size for quote (might get scaled smaller)
            max_words: str -- Maximum number of words per line for quote
            padding: str -- Padding between text and image boarder as a fraction
            gap: str -- Gap between quote body and author in pixels
        """
        self.base_path = base_path
        self.fnt_path = fnt_path
        self.fnt_size = fnt_size
        self.max_words = max_words
        self.padding = padding
        self.gap = gap

    def make_meme(self, img_path: str, text: str, author: str, width: int=500) -> str:
        """
        Create a meme from an image, text and author.
    
        Arguments:
            img_path: str -- path to the input image
            text: str -- text body of the quote
            author: str -- author of the quote
            width: int -- width of output image (defaul=500)
    
        Returns:
            out_path : str -- the file path to the output image
        """        
        self.load_image(img_path)
        self.resize_image(width)

        self.prepare_quote(text, author)
        self.add_quote()
        
        out_path = self.save_meme()
        return out_path

    def load_image(self, img_path: str) -> None:
        """Load image from path into class attribute."""
        self.image = Image.open(img_path)
        
    def resize_image(self, width: int) -> None:
        """Resize image to width."""
        if width is not None:
            height = self.image.size[1]*(width/self.image.size[0])
            self.image = self.image.resize((int(width), int(height)))
            
    def prepare_quote(self, body: str, author: str) -> None:
        """
        Prepare text and font sizes for quote.
        
        - Calls self.make_multiline() to break up long quotes into multiple lines.
        - Calls self.resize_fonts() to reduce font sizes until the quote fits.
        """
        self.str_body = f'"{self.make_multiline(body)}"'
        self.str_auth = f'- {author}'
        self.resize_fonts()

    def add_quote(self) -> None:
        """
        Add quote to meme.
        
        - Calls self.random_location() to get random coordinates that fit the dimensions.
        """
        d = ImageDraw.Draw(self.image)
        x_body, y_body, x_auth, y_auth = self.random_location()
        d.text((x_body, y_body), self.str_body, font=self.fnt_body, fill='white')
        d.text((x_auth, y_auth), self.str_auth, font=self.fnt_auth, fill='white')

    def save_meme(self) -> None:
        """
        Save the meme using a hash of the image as part of the file name.
        
        Returns:
            out_path: str -- path to saved meme
        """
        file_name = imagehash.average_hash(self.image)
        out_path = os.path.join(self.base_path,f'meme_{file_name}.jpg')
        self.image.save(out_path)
        return out_path

    def make_multiline(self, text: str) -> None:
        """Break up long quotes to multiple lines."""
        words = text.split()
        for i in range(self.max_words-1, len(words)-1, self.max_words):
            words[i] = words[i]+'\n'
        return ' '.join(words)
    
    def resize_fonts(self) -> None:
        """Reduce font size to ensure that the quote fits the image."""
        d = ImageDraw.Draw(self.image)
        while True:
            self.fnt_body = ImageFont.truetype(self.fnt_path, 
                                               int(self.fnt_size))
            self.fnt_auth = ImageFont.truetype(self.fnt_path, 
                                               int(self.fnt_size*2/3))
            
            _, _, w_body, h_body = d.textbbox((0, 0), 
                                              text=self.str_body,
                                              font=self.fnt_body)
            _, _, w_auth, h_auth = d.textbbox((0, 0), 
                                              text=self.str_auth,
                                              font=self.fnt_auth)
            if ((max(w_body, w_auth) < (1-2*self.padding)*self.image.size[0]) and 
                (h_body+h_auth+self.gap < (1-2*self.padding)*self.image.size[1])):
                break
            else:
                self.fnt_size -= 1
    
    def random_location(self) -> Tuple[int, int, int, int]:
        """
        Create coordinates for quote body and author on random location of the image.
        
        Returns:
            x_body, y_body, x_auth, y_auth -- coordinates of the quote body and author
        """
        d = ImageDraw.Draw(self.image)    
        _, _, w_body, h_body = d.textbbox((0, 0), 
                                          text=self.str_body,
                                          font=self.fnt_body)
        _, _, w_auth, h_auth = d.textbbox((0, 0), 
                                          text=self.str_auth,
                                          font=self.fnt_auth)
        
        w_both = max(w_body, w_auth)
        h_both = h_body+h_auth+self.gap
        
        x_body = randint(int(self.image.size[0]*self.padding), 
                    int(self.image.size[0]*(1-self.padding)-w_both))
        y_body = randint(int(self.image.size[1]*self.padding), 
                    int(self.image.size[1]*(1-self.padding)-h_both))
        x_auth = x_body
        y_auth = y_body + h_body + self.gap
        return x_body, y_body, x_auth, y_auth
    
"""
Implements the CLI interface.
"""
import os
import random
from argparse import ArgumentParser

from MemeEngine import MemeEngine
from QuoteEngine import QuoteModel, Ingestor

def generate_meme(path=None, body=None, author=None):
    """Generate a meme given an path and a quote."""
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            if not '.ipynb_checkpoints' in root:
                [imgs.append(os.path.join(root, name)) for name in files]

        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', type=str, help="Path to image file.")
    parser.add_argument('-b', '--body', type=str, help="Quote body.")
    parser.add_argument('-a', '--author', type=str, help="Quote author.")
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
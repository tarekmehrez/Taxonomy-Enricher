"""Contains string helper functions."""
import re
import difflib
from difflib import SequenceMatcher

from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer


def tokenize(text, language='english'):
    """
    Tokenize and process a given piece of text.

    - strip punctuations
    - strip extra spaces
    - lowercase
    - tokenize
    - apply snowball stemmer

    params:
        text (str)
        language (str) [default=english]

    returns:
       list[str]: tokenized and stemmed text
    """
    text = text.strip()

    # strip punctiations
    text = re.sub(r'[^\w\s]', '', text)

    # multiple spaces to one
    text = re.sub('[\s]+', ' ', text)

    # lower casing
    text = text.lower()

    # tokenize
    tokens = word_tokenize(text)

    # stemming
    stemmer = SnowballStemmer(language, ignore_stopwords=True)
    stemmed_tokens = [str(stemmer.stem(token)) for token in tokens]

    return stemmed_tokens


def most_similar(token, vocab):
    """
    Given a word and the entire vocab, get closest word in vocab.

    params:
        token (str)
        vocab (list[str])

    returns:
        str: most similar word
    """
    most_similar = difflib.get_close_matches(token, vocab)
    if most_similar == []:
        return ''
    else:
        return most_similar[0]


def similarity(token1, token2):
    """
    Get similarity between two tokens.

    params:
        token1 (str)
        token2 (str)

    returns:
        float
    """
    return SequenceMatcher(None, token1, token2).ratio()

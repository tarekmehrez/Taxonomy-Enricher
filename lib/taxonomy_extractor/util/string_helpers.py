"""Contains string helper functions."""
import string
import re
import difflib

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
    # strip punctiations
    text = text.translate(string.maketrans("", ""), string.punctuation)

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


def get_closest_word(token, vocab):
    """
    Given a word and the entire vocab, get closest word in vocab.

    params:
        token (str)
        vocab (list[str])

    returns:
        str: most similar word
    """
    return difflib.get_close_matches(token, vocab)[0]

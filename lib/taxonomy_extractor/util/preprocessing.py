"""Contains the preprocessing module."""
import string
import re


def tokenize(text):
    """
    Take in a piece of text, process and tokenize it.

    Args:
        text (str)
    Returns
       list[str]: tokenized text
    """
    # strip punctiations
    text = text.translate(string.maketrans("", ""), string.punctuation)

    # multiple spaces to one
    text = re.sub('[\s]+', ' ', text)

    # lower case
    text = text.lower()

    # now tokenize
    return text.split(' ')

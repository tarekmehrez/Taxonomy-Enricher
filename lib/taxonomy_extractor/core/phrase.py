"""Contains the phrase class."""
from taxonomy_extractor.util import string_helpers


class Phrase(object):

    """
    Create a phrase.

    - Save raw and tokenized form
    - Save word vectors on the token level and the phrase leve
    """

    def __init__(self, raw_form):
        """
        Initialize a phrase instance.

        params:
            raw_input(str): sequence of tokens as extracted from input
        """
        self.raw_form = raw_form.lower()
        self.tokens = string_helpers.tokenize(self.raw_form)

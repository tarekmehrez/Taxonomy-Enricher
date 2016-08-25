"""Contains the taxonomy class."""


class Taxonomy(object):

    """
    Creates a simple taxonomy object.
    """

    def __init__(self, id, head, synonyms):
        """
        Initialize a taxonomy instance.
        """
        self.id = id
        self.head = head
        self.synonyms = synonyms

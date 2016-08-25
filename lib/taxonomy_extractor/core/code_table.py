"""Contains the code table class."""
from taxonomy import Taxonomy
from phrase import Phrase
from taxonomy_extractor.util import string_helpers


class CodeTable(object):

    """
    Creates a code table that holds taxonomies.
    """

    def __init__(self):
        """
        Initialize a CodeTable instance.
        """
        self.taxonomies = {}
        self.attractors = {}

    def read(self, parsed_taxonomies):
        """
        Read in taxonomies for a given code table.

        params:
            taxonomies (dict{id: Taxonomy})
        """
        for key, taxonomy in parsed_taxonomies.iteritems():
            synonym_phrases = [Phrase(synonym)
                               for synonym in taxonomy.synonyms]

            head_phrase = Phrase(taxonomy.head)
            self.taxonomies[key] = Taxonomy(
                key, head_phrase, synonym_phrases)

    def collect_phrases(self):
        """
        Collect all phrases from code head and synonyms.

        returns:
            list[list[Phrase]]: collected phrases
        """
        total_phrases = []

        for taxonomy in self.taxonomies.values():
            total_phrases.append(taxonomy.head)
            total_phrases += [synonym for synonym in taxonomy.synonyms]

        return total_phrases

    def assign_early_attractors(self, phrases_dict):
        """
        Assign early attractors by using string similarity.

        params:
            phrases_dict (dict[str:Phrase]): keeps track of phrase strings and
                                             their respective Phrase objects
            threshold (float): minimum sim value to assign phrase to code.
        """
        for taxonomy in self.taxonomies.values():
            head = taxonomy.head.raw_form
            closest_phrase = string_helpers.most_similar(head,
                                                         phrases_dict.keys())

            if closest_phrase != '':
                # add it to taxonomy
                taxonomy.synonyms.append(phrases_dict[closest_phrase])

                # add it to currently attracted phrases
                self.attractors[closest_phrase] = taxonomy

    def assign_attractor(self, new_phrase, model, threshold):
        """
        Assign a new phrase to the table.

        params:
            new_phrase (Phrase)
            model (Word2Vec): trained vector space model
            threshold (float): minimum sim value to assign phrase to code.
        """
        closest_phrase, similarity = model.most_similar(new_phrase.raw_form,
                                                        self.attractors.keys())

        taxonomy = self.attractors[closest_phrase]

        if similarity < threshold:
            # add it to taxonomy
            taxonomy.synonyms.append(new_phrase)

            # add it to currently attracted phrases
            self.attractors[new_phrase.raw_form] = taxonomy

    def taxonomies_to_str(self):
        """
        Convert taxonomies to strings, to be written to a file.

        returns:
            taxonomies_as_str {dict:Taxonomy(str)}
        """
        taxonomies_as_str = {}
        for key, taxonomy in self.taxonomies.iteritems():
            taxonomy_head = taxonomy.head.raw_form
            synonyms = [synonym.raw_form for synonym in taxonomy.synonyms]

            taxonomies_as_str[key] = Taxonomy(key, taxonomy_head, synonyms)

        return taxonomies_as_str

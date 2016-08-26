"""Contains word2vec module."""
import operator

from gensim.models import Word2Vec as GensimWord2Vec
from taxonomy_extractor.util import math_helpers
from taxonomy_extractor.exceptions import PhraseNotInVocabError


class Word2Vec(object):

    """
    Train word2vec model.
    """

    def __init__(self):
        """
        Init wor2vec variables.
        """
        self.model = None
        self.phrases_model = {}

    def train(self, sentences, train_params={}):
        """
        Train word2vec model using gensim API.

        params:
            sentences list[list[str]]
            train_params dict: parameters passed to the word2vec gensim API

        returns:
            gensim.models.Word2Vec: trained model
        """
        print train_params
        self.model = GensimWord2Vec(sentences, **train_params)

    def create_phrase_model(self, phrases):
        """
        Create a phrase model, taking average of tokens forming phrases.

        params:
            phrases (list[Phrase])
        """
        for phrase in phrases:
            vectors = [self.model[token]
                       for token in phrase.tokens]

            self.phrases_model[
                phrase.raw_form] = math_helpers.average_vectors(vectors)

    def most_similar(self, phrase_str, other_phrases):
        """
        Return closest(similar) to a list of input words.

        params:
            phrase (str): input phrase
            count (str): number of returned results
        returns:
            (str, float): most similar word and it's cosine similarity
        """
        if phrase_str not in self.phrases_model.keys():
            raise PhraseNotInVocabError(
                'The phrase %s is not in vocab' % phrase_str)

        results = {}
        phrase_vector = self.phrases_model[phrase_str]

        for phrase in other_phrases:
            other_vector = self.phrases_model[phrase]
            sim = math_helpers.cosine_similarity(phrase_vector, other_vector)
            results[phrase] = sim

        if phrase_str in results:
            results.pop(phrase_str)
        sorted_results = sorted(results.items(), key=operator.itemgetter(1))
        return sorted_results[0]

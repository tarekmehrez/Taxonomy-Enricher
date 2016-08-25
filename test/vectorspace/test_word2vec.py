import unittest
from collections import namedtuple

from taxonomy_extractor.core import Phrase
from taxonomy_extractor.vectorspace import Word2Vec

TestCase = namedtuple('TestCase', ['input', 'expected'])
FLOAT_ROUND = 2

token_vectors = {'softwar': [0.50, 0.50, 0.40, 0.11, 0.04],
                 'engin': [0.79, 0.60, 0.53, 0.86, 0.58],
                 'develop': [0.45, 0.22, 0.5, 0.45, 0.79],
                 'manag': [0.89, 0.43, 0.08, 0.68, 0.02],
                 'director': [0.87, 0.93, 0.42, 0.20, 0.09]}

phrases = [Phrase('software engineer'),
           Phrase('software engineer manager'),
           Phrase('software developer'),
           Phrase('manager director')]

phrase_vectors = {'software engineer': [0.65, 0.55, 0.47, 0.48, 0.31],
                  'software engineer manager': [0.73, 0.51, 0.34, 0.55, 0.21],
                  'software developer': [0.47, 0.36, 0.45, 0.28, 0.42],
                  'manager director': [0.88, 0.68, 0.25, 0.44, 0.06]}


class TestWord2Vec(unittest.TestCase):

    def setUp(self):
        self.w2v = Word2Vec()
        self.w2v.model = token_vectors
        self.w2v.create_phrase_model(phrases)

    def test_create_phrase_model(self):
        self.assertDictAlmostEqual(self.w2v.phrases_model, phrase_vectors)

    def test_most_similar(self):
        test_cases = [
            TestCase(input='software engineer',
                     expected='software engineer manager'),
            TestCase(input='software engineer manager',
                     expected='software engineer'),
            TestCase(input='manager director',
                     expected='software engineer manager'),

        ]
        for case in test_cases:
            output = self.w2v.most_similar(case.input, phrase_vectors.keys())
            self.assertEqual(output[0], case.expected)

    def assertDictAlmostEqual(self, dict1, dict2):
        """
        Assert two lists almost equal.

        params:
            dict1 (dict{str:list[float]})
            dict2 (dict{str:list[float]})
        """
        self.assertListEqual(dict1.keys(), dict2.keys())
        for i, j in zip(dict1.keys(), dict2.keys()):
            self.assertListAlmostEqual(list(dict1[i]), list(dict2[j]))

    def assertListAlmostEqual(self, list1, list2):
        """
        Assert two lists almost equal.

        params:
            list1 (list[float])
            list2 (list[float])
        """
        for i, j in zip(list1, list2):
            rounded_i, rounded_j = self.round_values(i, j)
            self.assertAlmostEqual(rounded_i, rounded_j)

    def round_values(self, val1, val2):
        """
        Round values.

        params:
            val1 (float)
            val2 (float)
        """
        return round(val1, FLOAT_ROUND), round(val2, FLOAT_ROUND)

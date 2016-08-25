import unittest
from collections import namedtuple

from taxonomy_extractor.util import string_helpers

TestCase = namedtuple('TestCase', ['input', 'expected'])
FLOAT_ROUND = 2


class TestStringHelpers(unittest.TestCase):

    def test_tokenize(self):

        tokenizing_cases = [
            TestCase(
                input='Well, here is a STARTING point.',
                expected=[
                    'well',
                    'here',
                    'is',
                    'a',
                    'start',
                    'point']),

            TestCase(
                input='Software Development Engineer',
                expected=['softwar', 'develop', 'engin']),

            TestCase(
                input='Chief Executive Officer',
                expected=['chief', 'execut', 'offic']),


            TestCase(
                input='',
                expected=[])]

        for case in tokenizing_cases:
            output = string_helpers.tokenize(case.input)
            self.assertEqual(output, case.expected)

    def test_most_similar(self):

        vocab = ['software', 'engineer', 'developer']

        string_similarity_cases = [
            TestCase(input='sofwre', expected='software'),
            TestCase(input='engineering', expected='engineer'),
            TestCase(input='developement', expected='developer'),
            TestCase(input='analyst', expected=''),
        ]

        for case in string_similarity_cases:
            output = string_helpers.most_similar(case.input, vocab)
            self.assertEqual(output, case.expected)

    def test_similarity(self):
        string_similarity_cases = [
            TestCase(input=dict(token1='sofwre',
                                token2='software'),
                     expected=0.86),

            TestCase(input=dict(token1='engineering',
                                token2='engineer'),
                     expected=0.84),

            TestCase(input=dict(token1='developement',
                                token2='developer'),
                     expected=0.76),
        ]
        for case in string_similarity_cases:
            output = string_helpers.similarity(**case.input)

            rounded_expectation = round(case.expected, FLOAT_ROUND)
            rounded_output = round(output, FLOAT_ROUND)

            self.assertAlmostEqual(rounded_output, rounded_expectation)

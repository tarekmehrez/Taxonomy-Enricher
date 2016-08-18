import unittest
from collections import namedtuple

from taxonomy_extractor.util import string_helpers

TestCase = namedtuple('TestCase', ['input', 'expected'])


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

    def test_closest_word(self):

        vocab = ['software', 'engineer', 'developer']

        string_similarity_cases = [
            TestCase(input='sofwre', expected='software'),
            TestCase(input='engineering', expected='engineer'),
            TestCase(input='developement', expected='developer'),
        ]

        for case in string_similarity_cases:
            output = string_helpers.get_closest_word(case.input, vocab)
            self.assertEqual(output, case.expected)

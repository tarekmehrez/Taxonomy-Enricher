import unittest
from collections import namedtuple

from taxonomy_extractor.util import math_helpers

TestCase = namedtuple('TestCase', ['input', 'expected'])
FLOAT_ROUND = 2


class TestMathHelpers(unittest.TestCase):

    def test_average_vectors(self):

        test_cases = [
            TestCase(input=[[1, 2], [3, 4], [5, 6]],
                     expected=[3., 4.]),
            TestCase(input=[[0.5, 0.6, 0.7], [0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
                     expected=[0.33, 0.43, 0.53]),
        ]

        for case in test_cases:
            output = math_helpers.average_vectors(case.input)
            self.assertListAlmostEqual(output, case.expected)

    def test_cosine_similarity(self):
        test_cases = [
            TestCase(input=dict(vector1=[1, 2, 3], vector2=[1, 2, 3]),
                     expected=0.0),
            TestCase(input=dict(vector1=[1, 2, 3], vector2=[4, 5, 6]),
                     expected=0.03),
            TestCase(input=dict(vector1=[1, 2, 3], vector2=[1000, 4, 5]),
                     expected=0.73),
        ]
        for case in test_cases:
            output = math_helpers.cosine_similarity(**case.input)
            rounded_expectation, rounded_output = self.round_values(
                case.expected, output)
            self.assertAlmostEqual(rounded_output, rounded_expectation)

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

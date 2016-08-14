import unittest
from collections import namedtuple

from my_search.util import preprocessing

TestCase = namedtuple('TestCase', ['input', 'expected'])


tokenizing_cases = [TestCase(input='Well, here is a START.',
                             expected=['well', 'here', 'is', 'a', 'start']),

                    TestCase(input='Testing this- out',
                             expected=['testing', 'this', 'out']),

                    TestCase(input='',
                             expected=[''])]


class TestPreprocessing(unittest.TestCase):

    def test_tokenize(self):
        for case in tokenizing_cases:
            output = preprocessing.tokenize(case.input)
            self.assertEqual(output, case.expected)

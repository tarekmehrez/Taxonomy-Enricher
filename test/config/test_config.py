import unittest

from tempfile_helper import create_temp_file
from taxonomy_extractor.config import Parser


config_str = """[default]
filled_taxonomies = file_1.xml
                    file_2.tsv
                    file_3.tsv

empty_taxonomies = input.tsv

output_taxonomies = output.tsv

[word2vec]
mode = train
"""


config_dict = {'filled_taxonomies': ['file_1.xml',
                                     'file_2.tsv',
                                     'file_3.tsv'],
               'empty_taxonomies': ['input.tsv'],
               'output_taxonomies': ['output.tsv']}


config_dict = {
    'default': {
        'output_taxonomies': ['output.tsv'],
        'filled_taxonomies': [
            'file_1.xml',
            'file_2.tsv',
            'file_3.tsv'],
        'language': 'english',
        'empty_taxonomies': ['input.tsv']},
    'word2vec': {
        'workers': 4,
        'negative': 5,
        'window': 5,
        'mode': 'train',
                'alpha': 0.025,
                'min_count': 0,
        'size': 50}}


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_parse_config(self):
        temp_file = create_temp_file(config_str, '.ini')
        self.parser.parse_config(temp_file)
        output = self.parser.config_to_dict()

        self.assertDictEqual(output, config_dict)
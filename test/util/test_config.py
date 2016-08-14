import unittest

from tempfile_helper import create_temp_file
from taxonomy_extractor.util import config


config_str = """[default]
filled_taxonomies = file_1.xml
                    file_2.tsv
                    file_3.tsv

empty_taxonomies = input.tsv

output_taxonomies = output.tsv"""


config_dict = {'filled_taxonomies': ['file_1.xml',
                                     'file_2.tsv',
                                     'file_3.tsv'],
               'empty_taxonomies': ['input.tsv'],
               'output_taxonomies': ['output.tsv']}


class TestConfig(unittest.TestCase):

    def test_parse_config(self):
        temp_file = create_temp_file(config_str, '.ini')
        output = config.parse_config(temp_file)

        self.assertDictEqual(output, config_dict)

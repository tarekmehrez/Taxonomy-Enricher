import unittest

from taxonomy_extractor.core import Phrase
from taxonomy_extractor.core import Taxonomy
from taxonomy_extractor.core import CodeTable

id_str = 'SDE'

head_str = 'software engineer'
head_phrase = Phrase(head_str)

synonyms_str = ['software developer',
                'computer scientist',
                'application developer',
                'backend developer']

synonyms_phrases = [Phrase(token) for token in synonyms_str]

parsed_taxonomy = {id_str: Taxonomy(id_str, head_str, synonyms_str)}
phrases_taxonomy = {id_str: Taxonomy(id_str, head_phrase, synonyms_phrases)}

empty_taxonomies = {'SDE': Taxonomy('SDE', 'software engineer', []),
                    'BI': Taxonomy('BI', 'bus. intelligence specialist', []),
                    'FA': Taxonomy('BI', 'finanical analyst', [])}


to_be_filled = {'Junior Analyst': Phrase('Junior Analyst'),
                'Backend Engineer': Phrase('Backend Engineer')}


class TestCodeTable(unittest.TestCase):

    def setUp(self):
        self.table = CodeTable()

    def test_read_code_table(self):
        self.table.read(parsed_taxonomy)

        output_phrases_taxonomy = self.table.taxonomies[id_str]
        expected_phrases_taxonomy = phrases_taxonomy[id_str]

        self.assertEqual(output_phrases_taxonomy.id,
                         expected_phrases_taxonomy.id)

        self.assertDictEqual(output_phrases_taxonomy.head.__dict__,
                             expected_phrases_taxonomy.head.__dict__)

        for output, expected in zip(output_phrases_taxonomy.synonyms,
                                    expected_phrases_taxonomy.synonyms):

            self.assertDictEqual(output.__dict__, expected.__dict__)

    def test_collect_phrases(self):
        self.table.read(parsed_taxonomy)

        expected_phrases = [head_phrase] + synonyms_phrases
        output_phrases = self.table.collect_phrases()
        for output, expected in zip(output_phrases, expected_phrases):
            self.assertDictEqual(output.__dict__, expected.__dict__)

    def test_assign_early_attractors(self):
        self.table.read(empty_taxonomies)
        self.table.assign_early_attractors(to_be_filled)

        expected_taxonomies = {'Backend Engineer': empty_taxonomies['SDE'],
                               'Junior Analyst': empty_taxonomies['FA']}

        for phrase_str, taxonomy in self.table.attractors.iteritems():
            expected_attracted_phrase = expected_taxonomies[phrase_str].head
            output_attracted_phrase = taxonomy.head.raw_form

            self.assertEqual(output_attracted_phrase,
                             expected_attracted_phrase)

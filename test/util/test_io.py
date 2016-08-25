# -*- coding: utf-8 -*-
import unittest
from nose.tools import raises
from collections import namedtuple

from ..tempfile_helper import declare_temp_file
from ..tempfile_helper import create_temp_file
from taxonomy_extractor.util import io
from taxonomy_extractor.exceptions import UnrecognizedFileExtensionError


Taxonomy = namedtuple('Taxonomy', ['id', 'head', 'synonyms'])
TestCase = namedtuple('TestCase', ['input', 'expected'])


taxonomy_dict = {u'SDE': dict(id=u'SDE',
                              head=u'software engineer',
                              synonyms=[u'software developer',
                                        u'computer scientist',
                                        u'application developer',
                                        u'backend developer'])}

taxonomy_tsv = ('SDE\tsoftware engineer\n'
                '-\tsoftware developer\n'
                '-\tcomputer scientist\n'
                '-\tapplication developer\n'
                '-\tbackend developer\n')

taxonomy_xml = """<?xml version="1.0"?>
                    <CodeTable>
                    <CodeTableInfo>
                    <InfoItem name="date">22-11-2005</InfoItem>
                    </CodeTableInfo>
                    <CodeRecordList>
                    <CodeRecord>
                    <CodeID>SDE</CodeID>
                    <CodeDescription>software engineer</CodeDescription>
                    <CodeProperty name="codeid">SDE</CodeProperty>
                    <CodeProperty name="description">software engineer</CodeProperty>
                    <InstanceList>
                    <Instance>
                    <InstanceDescription>software developer</InstanceDescription>
                    </Instance>
                    <Instance>
                    <InstanceDescription>computer scientist</InstanceDescription>
                    </Instance>
                    <Instance>
                    <InstanceDescription>application developer</InstanceDescription>
                    </Instance>
                    <Instance>
                    <InstanceDescription>backend developer</InstanceDescription>
                    </Instance>
                    </InstanceList>
                    </CodeRecord>
                    </CodeRecordList>
                    </CodeTable>"""

code_table_tsv = ('SDE\tSoftware Developer\n'
                  'BI\tBusiness Inteligence Specialist\n'
                  'FA\tFinancial Analyst\n')


code_table_dict = {'SDE': dict(id='SDE',
                               head='Software Developer',
                               synonyms=[]),
                   'BI': dict(id='BI',
                              head='Business Inteligence Specialist',
                              synonyms=[]),
                   'FA': dict(id='FA',
                              head='Financial Analyst',
                              synonyms=[]), }


class TestIO(unittest.TestCase):

    def test_read_filled_xml_taxonomy(self):
        temp_file = create_temp_file(taxonomy_xml, '.xml')
        output = io.read(temp_file)

        for key in output:
            self.assertDictEqual(output[key].__dict__, taxonomy_dict[key])

    def test_read_filled_tsv_taxonomy(self):
        temp_file = create_temp_file(taxonomy_tsv, '.tsv')
        output = io.read(temp_file)

        for key in output:
            self.assertDictEqual(output[key].__dict__, taxonomy_dict[key])

    def test_read_empty_tsv_taxonomy(self):
        temp_file = create_temp_file(code_table_tsv, '.tsv')
        output = io.read(temp_file)

        for key in output:
            self.assertDictEqual(output[key].__dict__, code_table_dict[key])

    def test_write_filled_tsv_taxonomy(self):
        temp_file = declare_temp_file('.tsv')

        # create objects from the dict (as expected by the io.py module)
        objects = {}
        for key in taxonomy_dict:
            objects[key] = Taxonomy(**taxonomy_dict[key])

        # then write created objects
        io.write(objects, temp_file)
        output = io.read(temp_file)

        for key in output:
            self.assertDictEqual(output[key].__dict__, taxonomy_dict[key])

    def test_encoding(self):
        test_cases = [
            TestCase(input=u'co\xf6rdinator',
                     expected='coördinator'),
            TestCase(input=u't\xe4tigkeit',
                     expected='tätigkeit',),
            TestCase(input=[u'co\xf6rdinator', u't\xe4tigkeit'],
                     expected=['coördinator', 'tätigkeit'],),
        ]

        for case in test_cases:
            output = io.encode(case.input)
            self.assertEquals(output, case.expected)

    def test_decoding(self):
        test_cases = [
            TestCase(input='coördinator',
                     expected=u'co\xf6rdinator'),
            TestCase(input='tätigkeit',
                     expected=u't\xe4tigkeit'),
            TestCase(input=['coördinator', 'tätigkeit'],
                     expected=[u'co\xf6rdinator', u't\xe4tigkeit']),
        ]

        for case in test_cases:
            output = io.decode(case.input)
            self.assertEquals(output, case.expected)

    @raises(UnrecognizedFileExtensionError)
    def test_read_wrong_extension(self):
        temp_file = create_temp_file(taxonomy_tsv, '.json')
        io.read(temp_file)

    @raises(UnrecognizedFileExtensionError)
    def test_write_wrong_extension(self):
        io.write(taxonomy_dict, 'temp.json')

import unittest
import tempfile
from nose.tools import raises
from collections import namedtuple

from taxonomy_extractor.util import io
from taxonomy_extractor.exceptions import UnrecognizedFileExtensionError


Taxonomy = namedtuple('Taxonomy', ['id', 'head', 'synonyms'])


taxonomy_dict = {'SDE': Taxonomy(id='SDE',
                                 head='software engineer',
                                 synonyms=['software developer',
                                           'computer scientist',
                                           'application developer',
                                           'backend developer'])}

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


code_table_dict = {'SDE': Taxonomy(id='SDE',
                                   head='Software Developer',
                                   synonyms=[]),
                   'BI': Taxonomy(id='BI',
                                  head='Business Inteligence Specialist',
                                  synonyms=[]),
                   'FA': Taxonomy(id='FA',
                                  head='Financial Analyst',
                                  synonyms=[]), }


class TestIO(unittest.TestCase):

    def test_read_filled_xml_taxonomy(self):
        temp_file = self.create_temp_file(taxonomy_xml, '.xml')
        output = io.read(temp_file)

        self.assertDictEqual(output, taxonomy_dict)

    def test_read_filled_tsv_taxonomy(self):
        temp_file = self.create_temp_file(taxonomy_tsv, '.tsv')
        output = io.read(temp_file)

        self.assertDictEqual(output, taxonomy_dict)

    def test_read_empty_tsv_taxonomy(self):
        temp_file = self.create_temp_file(code_table_tsv, '.tsv')
        output = io.read(temp_file)

        self.assertDictEqual(output, code_table_dict)

    def test_write_filled_tsv_taxonomy(self):
        temp_file = self.declare_temp_file('.tsv')

        io.write(taxonomy_dict, temp_file)
        output = io.read(temp_file)

        self.assertDictEqual(output, taxonomy_dict)

    @raises(UnrecognizedFileExtensionError)
    def test_read_wrong_extension(self):
        temp_file = self.create_temp_file(taxonomy_tsv, '.json')
        io.read(temp_file)

    @raises(UnrecognizedFileExtensionError)
    def test_write_wrong_extension(self):
        io.write(taxonomy_dict, 'temp.json')

    def create_temp_file(self, content, extension):
        """
        Create a temp file with some content and extension.

        params:
            content (obj): file content to write
            extension (str): file extension preceded by a dot

        returns:
            file's name

        """
        temp_file = self.declare_temp_file(extension)
        with open(temp_file, mode='wb') as f:
            f.write(content)

        return temp_file

    def declare_temp_file(self, extension):
        """
        Create an empty temp file.

        params: see self.create_temp_file
        returns: see self.create_temp_file
        """
        temp_file = tempfile.NamedTemporaryFile(suffix=extension, delete=False)
        return temp_file.name

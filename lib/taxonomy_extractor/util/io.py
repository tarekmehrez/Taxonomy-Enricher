"""Contains the io module that reads in tsv and xml files."""
import os
import csv
from collections import namedtuple

from ConfigParser import SafeConfigParser
from lxml import etree

from taxonomy_extractor.exceptions import UnrecognizedFileExtensionError


Taxonomy = namedtuple('Taxonomy', ['id', 'head', 'synonyms'])
CODE_XML_TAG = 'CodeRecord'
CODE_ID_XML_TAG = 'CodeID'
CODE_DESCRIPTION_XML_TAG = 'CodeDescription'
INSTANCE_DESCRIPTION_XML_TAG = 'InstanceDescription'


def get_extension(file_path):
    """
    Get extension of the file.

    params:
        file_path(str): path to file

    returns:
        str: extension preceded by a dot (e.g .xml)
    """
    _, extension = os.path.splitext(file_path)
    return extension


def write(file_content, file_path):
    """
    Write taxonomies to different formats.

    params:
        file_content (dict{id: Taxonomy})
        file_path (str)
    """
    extension = get_extension(file_path)

    if extension == '.tsv':
        _write_tsv(file_content, file_path)
    else:
        raise UnrecognizedFileExtensionError(
            'Extension %s is not recognized' % extension)


def _write_tsv(file_content, file_path):
    """
    Write taxonomies to tsv file.

    params: see util/io.py::write
    """
    with open(file_path, 'wb') as f:
        for _, taxonomy in file_content.iteritems():
            f.write('%s\t%s\n' % (taxonomy.id, taxonomy.head))

            for synonym in taxonomy.synonyms:
                f.write('-\t%s\n' % synonym)


def read(file_path):
    """
    Read taxonomies in different formats.

    params:
        file_path: (str) path to input file
    returns:
        obj: content of the file
    """
    extension = get_extension(file_path)

    if extension == '.xml':
        content = _read_xml(file_path)

    elif extension == '.tsv':
        content = _read_tsv(file_path)

    elif extension == '.ini':
        content = _read_ini(file_path)

    else:
        raise UnrecognizedFileExtensionError(
            'Extension %s is not recognized' % extension)

    return content


def _read_ini(file_path):
    """
    Read ini config files.

    params: see util/io.py::read
    returns: see util/io.py::read
    """
    parser = SafeConfigParser()
    parser.read(file_path)

    return parser


def _read_tsv(file_path):
    """
    Read list of taxonomies from a normalized tsv file.

    Example format (.tsv):
    ID  taxonomy head
    -   synonym1
    -   synonym2

    params: see util/io.py::read
    returns: see util/io.py::read
    """
    with open(file_path) as f:
        rows = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

        taxonomies = {}

        for row in rows:
            taxonomy_id, token = row

            # new taxonomy head
            if taxonomy_id != '-':
                current_taxonomy = Taxonomy(taxonomy_id, token, synonyms=[])
                taxonomies[taxonomy_id] = current_taxonomy

            #  new synonym
            else:
                current_taxonomy.synonyms.append(token)

        return taxonomies


def _read_xml(file_path):
    """
    Read in taxonomies from xml file.

    params: see util/io.py::read
    returns: see util/io.py::read
    """
    taxonomies = {}
    tree = etree.parse(file_path)
    codes = tree.xpath('.//%s' % CODE_XML_TAG)

    for code in codes:
        taxonomy_id, taxonomy_head, synonyms = _extract_taxonomy(code)
        taxonomies[taxonomy_id] = Taxonomy(
            taxonomy_id, taxonomy_head, synonyms)

    return taxonomies


def _extract_taxonomy(etree):
    """
    Given a code xml etree, extract its id, head and synonyms.

    params:
        etree (lxml etree)
    returns
        str: id
        str: taxonomy head token
        list[str]: synonyms tokens
    """
    head_as_etrees = etree.xpath('.//%s' % CODE_DESCRIPTION_XML_TAG)
    id_as_etrees = etree.xpath('.//%s' % CODE_ID_XML_TAG)
    synonyms_as_etrees = etree.xpath('.//%s' % INSTANCE_DESCRIPTION_XML_TAG)

    # taking first element since the list size is 1
    head_as_str = head_as_etrees[0].text
    id_as_str = id_as_etrees[0].text
    synonyms_as_str = [synonym.text for synonym in synonyms_as_etrees]

    return id_as_str, head_as_str, synonyms_as_str

"""Contains the config module."""
from taxonomy_extractor.util import io


def parse_config(file_path):
    """
    Read and parse the config file.

    params:
        file_path (str): path to config file

    returns:
        dict{str:list[str]}: parsed config as a dict
    """
    config_dict = {}

    parser = io.read(file_path)

    config_dict['filled_taxonomies'] = parser.get(
        'default', 'filled_taxonomies').split('\n')

    config_dict['empty_taxonomies'] = parser.get(
        'default', 'empty_taxonomies').split('\n')

    config_dict['output_taxonomies'] = parser.get(
        'default', 'output_taxonomies').split('\n')

    return config_dict

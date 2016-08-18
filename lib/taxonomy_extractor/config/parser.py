"""Contains the config module."""
from collections import defaultdict

import helpers
from taxonomy_extractor.util import io
from taxonomy_extractor.exceptions import RequiredConfigOptionNotFoundError


class Parser(object):

    """
    Parse .ini config files.
    """

    def __init__(self):
        """
        Initialize config options.
        """
        self.options = helpers.add_options()
        self.parser = None

    def parse_config(self, file_path):
        """
        Read and parse the config file.

        params:
            file_path (str): path to config file

        returns:
            dict{str:list[str]}: parsed config as a dict
        """
        self.parser = io.read(file_path)

        for option in self.options:
            if option.required:
                self._parse_required(option)
            else:
                self._parse_optional(option)

    def _parse_required(self, option):
        """
        Parse required config option.

        params:
            option (Option)
        """
        if self.parser.has_option(option.section, option.param):
            option.set_value(self.parser.get(option.section, option.param))
        else:
            raise RequiredConfigOptionNotFoundError(
                '%s:%s is required but is not found' %
                (option.section,
                 option.param))

    def _parse_optional(self, option):
        """
        Parse optional config option.

        params:
            option (Option)
        """
        if self.parser.has_option(option.section, option.param):
            option.set_value(self.parser.get(option.section, option.param))

    def config_to_dict(self):
        """
        Convert parsed values to dict.

        returns:
            dict: parsed config items
        """
        config_dict = defaultdict(lambda: {})

        for option in self.options:
            config_dict[option.section][option.param] = option.value

        return config_dict

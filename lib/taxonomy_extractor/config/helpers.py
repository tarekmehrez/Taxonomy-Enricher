"""Helper functions for config module."""
from option import Option


def add_options():
    """
    Add expected config params.

    returns:
        list[options]
    """
    options = []

    options.append(Option(section='default',
                          param='filled_taxonomies',
                          type=(list, str),
                          required=True,
                          default_value=None))

    options.append(Option(section='default',
                          param='empty_taxonomies',
                          type=(list, str),
                          required=True,
                          default_value=None))

    options.append(Option(section='default',
                          param='output_taxonomies',
                          type=(list, str),
                          required=True,
                          default_value=None))

    options.append(Option(section='default',
                          param='language',
                          type=str,
                          required=False,
                          default_value='english'))

    # word2vec options
    options.append(Option(section='word2vec',
                          param='mode',
                          type=str,
                          required=True,
                          default_value=None))

    options.append(Option(section='word2vec',
                          param='min_count',
                          type=int,
                          required=False,
                          default_value=0))

    options.append(Option(section='word2vec',
                          param='window',
                          type=int,
                          required=False,
                          default_value=5))

    options.append(Option(section='word2vec',
                          param='negative',
                          type=int,
                          required=False,
                          default_value=5))

    options.append(Option(section='word2vec',
                          param='size',
                          type=int,
                          required=False,
                          default_value=50))

    options.append(Option(section='word2vec',
                          param='alpha',
                          type=float,
                          required=False,
                          default_value=0.025))

    options.append(Option(section='word2vec',
                          param='workers',
                          type=int,
                          required=False,
                          default_value=4))

    return options

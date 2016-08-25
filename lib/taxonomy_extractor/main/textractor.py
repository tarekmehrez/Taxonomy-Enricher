"""Contains the main textractor class."""

from taxonomy_extractor.core import CodeTable
from taxonomy_extractor.vectorspace import word2vec
from taxonomy_extractor.util import io
from taxonomy_extractor.util import logger

logger = logger.init_logger()


class Textractor(object):

    """
    Textractor class.

    - Reads in input code tables
    - traing vector space model
    - use model + string similarity to fill in new tables
    """

    def __init__(self):
        """
        Initialize a textractor instance.
        """
        self.input_tables = []
        self.output_table = None
        self.total_phrases = []
        self.vector_space_model = None

    def run(self, parsed_config):
        """
        Run the textractor module.

        params:
            parsed_config (dict)
        """
        logger.debug('Starting Textractor')

        self.read_input_tables(parsed_config['default']['filled_taxonomies'])
        self.train_vector_space(
            parsed_config['word2vec'],
            parsed_config['default']['vector_space_output'])
        self.read_output_table(parsed_config['default']['empty_taxonomies'])
        self.fill_output_tables(parsed_config['default']['vector_threshold'])
        self.write_output_tables(parsed_config['default']['output_taxonomies'])

    def read_input_tables(self, input_tables_paths):
        """
        Read in input tables.

        params:
            input_tables_paths (list[str])
        """
        logger.info('Reading in input tables %s' % input_tables_paths)
        for path in input_tables_paths:
            self.input_tables.append(self._read_table(path))

    def read_output_table(self, output_table_path):
        """
        Read in output table.

        params:
            output_table_path (str)
        """
        logger.info('Reading in output table to be filled %s' %
                    output_table_path)
        self.output_table = self._read_table(output_table_path)

    def write_output_tables(self, output_table_path):
        """
        Write filled tables to the output path.

        params:
            output_table_path (str)
        """
        logger.info('Writing output table to %s' % output_table_path)
        self._write_table(
            self.output_table.taxonomies_to_str(), output_table_path)

    def _read_table(self, path):
        """
        Read in a single table.

        - Parse taxonomies
        - Create a CodeTable instance
        - Assign taxonomies to the new CodeTable

        params:
            path (str)
        """
        parsed_taxonomies = io.read(path)
        table = CodeTable()
        table.read(parsed_taxonomies)
        return table

    def _write_table(self, table, path):
        """
        Write CodeTable to the given path.

        params:
            table (CodeTable)
            path (str)
        """
        io.write(table, path)

    def train_vector_space(self, train_params, output_path):
        """
        Train vector space model.

        params:
            train_params (dict)
        """
        if io.exists(output_path):
            logger.debug('Vector space already exists, loading %s' %
                         output_path)
            self.vector_space_model = io.read(output_path)
        else:
            logger.info('Training vector space using word2vec')
            self._collect_phrases()
            phrases_as_tokens = self._phrases_to_tokens()
            self._start_word2vec(phrases_as_tokens, train_params)
            self._assign_vectors_to_phrases()
            logger.debug('Writing vector space to %s' %
                         output_path)

            io.write(self.vector_space_model, output_path)

    def _start_word2vec(self, phrases_as_tokens, train_params):
        """
        Start word2vec training.

        Phrases as tokens represent each taxonomy as series of tokens.
        Example:
        + Software Engineer
        - Software Developer
        - Backend Developer

        will be represented as: [software, engineer, software, developer, ..]

        params:
            phrases_as_tokens (list[list[str]])
            train_params (dict)
        """
        logger.debug('Starting word2vec')
        self.vector_space_model = word2vec.Word2Vec()
        self.vector_space_model.train(phrases_as_tokens, train_params)

    def _assign_vectors_to_phrases(self):
        """
        Assign vectors to phrases after training.

        Since training is done on the token level, each phrase will get
        a vector based on its tokens' vectors, by taking their average
        """
        logger.debug(
            'Converting vector space model from token level to phrase level')

        self.vector_space_model.create_phrase_model(self.total_phrases)

    def fill_output_tables(self, vector_threshold):
        """
        Fill output tables with new phrases.
        """
        logger.info('Filling output tables')

        phrases_dict = self._phrases_to_dict()

        logger.debug('Assigning early attractors using string similarity')
        self.output_table.assign_early_attractors(phrases_dict)

        logger.debug('Assigning remaining phrases using vector similarity')
        for phrase_obj in phrases_dict.values():
            self.output_table.assign_attractor(phrase_obj,
                                               self.vector_space_model,
                                               vector_threshold)

    def _collect_phrases(self):
        """
        Collect phrases from input tables.

        self.total_phrases should then be a huge list of Phrase objects
        """
        logger.debug('Collecting phrase from input tables')
        for table in self.input_tables:
            self.total_phrases += table.collect_phrases()

    def _phrases_to_tokens(self):
        """
        Create a list of tokens representing the phrase list.

        returns:
            list[list[str]]
        """
        logger.debug('Collecting phrase tokens for training')
        phrases_as_tokens = []
        for phrase in self.total_phrases:
            phrases_as_tokens.append(phrase.tokens)

        return phrases_as_tokens

    def _phrases_to_dict(self):
        """
        Create a dict of phrases str and their object references.

        returns:
            dict{str:Phrase}
        """
        logger.debug(
            'Creating <phrase_str, phrase_ref> dict to fill output table')

        phrases_dict = {}
        for phrase in self.total_phrases:
            phrases_dict[phrase.raw_form] = phrase

        return phrases_dict

"""Contains package-specific extensions."""


class UnrecognizedFileExtensionError(Exception):

    """
    Unrecognized file extension error.
    """

    pass


class LanguageNotSupportedError(Exception):

    """
    Language not supported error.
    """

    pass


class RequiredConfigOptionNotFoundError(Exception):

    """
    Required config option not found error.
    """

    pass


class PhraseNotInVocabError(Exception):

    """
    Phrase not found in vocab error.
    """

    pass

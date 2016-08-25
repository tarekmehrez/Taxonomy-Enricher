"""Contains the logger module."""
import logging


def init_logger():
    """
    Initialize and return logger.

    returns:
        logger
    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s : %(levelname)s : %(message)s')
    logger = logging.getLogger(__name__)
    return logger


def get_logger():
    """
    Get current logger.

    returns:
        logger
    """
    logger = logging.getLogger(__name__)
    return logger

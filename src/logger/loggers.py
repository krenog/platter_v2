import logging

from .filters import AddDjangoRequestFilter


def platter_logger():
    logger = logging.getLogger('platter')
    dgs_filter = AddDjangoRequestFilter()
    logger.addFilter(dgs_filter)
    return logger

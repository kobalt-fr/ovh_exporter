"""Logger configuration."""

import logging

log = logging.getLogger("ovh_exporter")


def init_logging(level: int = logging.WARNING):
    """Init logging configuration."""
    logging.basicConfig()
    log.setLevel(level)

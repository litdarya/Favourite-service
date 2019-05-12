import logging
from logging import Logger
from typing import Dict, Any

import logstash
from favourite.settings import LOGSTASH


def _get_logstash_handler() -> logstash.TCPLogstashHandler:
    return logstash.TCPLogstashHandler(**LOGSTASH)


def _get_logger() -> Logger:
    _logger = logging.getLogger(__name__)
    _logger.addHandler(_get_logstash_handler())
    return _logger


logger: Logger = _get_logger()


def log(exception: Exception, extra: Dict[str, Any]):
    logger.exception(exception, extra=extra)



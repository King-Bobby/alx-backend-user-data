#!/usr/bin/env python3
"""Module filtered_logger.py"""

import re
import logging
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initialzie the class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format function"""
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields,
                            self.REDACTION, message, self.SEPARATOR)


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    field_pattern = '|'.join(fields)
    return re.sub(fr'({separator}{field_pattern}=[^;]*)(?={separator}|$)',
                  f'{separator}{redaction}', message)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object for user_data."""
    logger = logging.getLogger("user_data")
    logging.setLevel(logging.INFO)
    logging.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger

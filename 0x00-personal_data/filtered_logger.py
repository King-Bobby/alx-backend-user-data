#!/usr/bin/env python3
"""Module filtered_logger.py"""

import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    field_pattern = '|'.join(fields)
    return re.sub(fr'({separator}{field_pattern}=[^;]*)(?={separator}|$)',
                  f'{separator}{redaction}', message)

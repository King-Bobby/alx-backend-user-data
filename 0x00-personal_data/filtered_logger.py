#!/usr/bin/env python3
"""Module filtered_logger.py"""

import os
import mysql.connector
from mysql.connector import MySQLConnection
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

    # Create a StreamHandler with RedactingFormatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """Returns a connector to the database."""
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    database_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    # create a MySQL connection
    db = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database_name
    )
    return db


def main():
    """the main function"""
    logger = logging.getLogger("user_data")
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        filtered_row = {k: "***" if k in PII_FIELDS
                        else v for k, v in row.items()}
        log_message = "[HOLBERTON] user_data INFO %s: %s;" % (
                row["last_login"].isoformat(), filtered_row)
        logger.info(log_message)

    cursor.close()
    db.close()

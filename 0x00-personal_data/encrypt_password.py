#!/usr/bin/env python3
"""Module encrypt.py"""

import bcrypt


def hash_password(password: str) -> bytes:
    """expects one string argument and returns a salted, hashed password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

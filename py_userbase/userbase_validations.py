#!/usr/bin/python
"""User Validations"""
import userbase_models
from validate_email import validate_email
import string

def display_name(display_name):
    """ validates displayName """
    if len(display_name) < 3:
        return False
    return True

def email(email):
    """ validates email """
    return validate_email(email)

def password(password):
    """ validates password """
    if len(password) < 6:
        return False
    return set(password).issubset(set(string.printable))

def username(username):
    """ validates username """
    if len(username) < 3:
        return False
    return set(username).issubset(set(string.ascii_letters + string.digits))

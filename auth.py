import bcrypt
from db import db_handler


def authenticate(username, password):
    """Check that unhashed password matches the stored hash in database"""
    password = bytes(password, 'utf-8')
    stored_hash = bytes(db_handler.get_password_hash_for_username(username))
    if bcrypt.checkpw(password, stored_hash):
        return True
    else:
        return False

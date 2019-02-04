import bcrypt
from db import db_handler


def login(username, password):
    """Check that unhashed password matches hash stored in database"""
    password = bytes(password, 'utf-8')
    stored_hash = bytes(db_handler.get_password_hash_for_username(username))
    if bcrypt.checkpw(password, stored_hash):
        return True
    else:
        return False


def register(form):
    password = bytes(form.get('password'), 'utf-8')
    password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
    db_handler.add_user(
        username=form.get('username'),
        password_hash=password_hash,
        email=form.get('email'),
        first_name=form.get('first_name'),
        last_name=form.get('last_name'),
        locality=form.get('locality'),
        country=form.get('country'),
        facebook_username=form.get('facebook_username'),
        github_username=form.get('github_username'),
        twitter_username=form.get('twitter_username'),
        linkedin_profile_url=form.get('linkedin_profile_url'),
    )

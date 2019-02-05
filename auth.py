import bcrypt
from db import db_handler
from functools import wraps
from flask import render_template


def login(username, password):
    """Retrieve user info from db, compare hashes, return user info on match else `False`"""
    password = bytes(password, 'utf-8')
    try:
        user_info = db_handler.get_user_info(username)
    except IndexError:
        return False
    stored_hash = user_info.get('password_hash')
    if bcrypt.checkpw(password, stored_hash):
        return user_info
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


def needs_login(session):
    def inner(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if 'username' in session:
                return fn(*args, **kwargs)
            else:
                return render_template('login.html', message='You need to log in to access this functionality.')
        return wrapper
    return inner

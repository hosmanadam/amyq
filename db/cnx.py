import os
from functools import wraps

import mysql.connector


LOCAL = {
    'host':     os.environ.get('local_host'),
    'database': os.environ.get('local_database'),
    'user':     os.environ.get('local_user'),
    'password': os.environ.get('local_password')
}

REMOTE = {
    'host':     os.environ.get('remote_host'),
    'database': os.environ.get('remote_database'),
    'user':     os.environ.get('remote_user'),
    'password': os.environ.get('remote_password')
}


def get_connection(remote=False):
    """
    Return `MySQL connection object` connecting to one of two MySQL servers

    :param bool remote: Run on server configured as `REMOTE` if `True`, else on `LOCAL`
    :rtype: MySQL connection object
    :return: Connection to one of two MySQL servers
    """
    if remote:
        return mysql.connector.connect(**REMOTE)
    else:
        return mysql.connector.connect(**LOCAL)


def connection_handler(dictionary=False):
    """
    Open & close database connection for decorated function, unless caller has passed one already

    :param bool dictionary: Make dictionary cursor instead of default list cursor
    :rtype: function
    :return: Decorated function
    """
    def inner(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if any('MySQLCursor' in str(type(arg)) for arg in args):
                return fn(*args, **kwargs)
            else:
                connection = get_connection()
                connection.autocommit = False
                cursor = connection.cursor(dictionary=dictionary)
                result = fn(connection, cursor, *args, **kwargs)
                connection.commit()
                cursor.close()
                connection.close()
                return result
        return wrapper
    return inner

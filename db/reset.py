from cnx import connection_handler
from util import break_up_query


@connection_handler()
def list_all_tables(connection, cursor):
    cursor.execute("SHOW TABLES")
    return list(table[0] for table in cursor.fetchall())


@connection_handler()
def drop_tables(connection, cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    for table in list_all_tables():
        cursor.execute(f"DROP TABLE {table}")
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")


@connection_handler()
def rebuild_tables(connection, cursor):
    with open('db/schema.sql', 'r') as file:
        multi_query = file.read()
        for query in break_up_query(multi_query):
            cursor.execute(query)


@connection_handler()
def populate_tables(connection, cursor):
    with open('db/starter_data.sql', 'r') as file:
        multi_query = file.read()
        for query in break_up_query(multi_query):
            cursor.execute(query)


def reset_database():
    """Reset full database by dropping, rebuilding and importing data to tables"""
    drop_tables()
    rebuild_tables()
    populate_tables()
    print("\nReset finished!")

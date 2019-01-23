def break_up_query(multi_query):
    """
    Return list of individual SQL statements in `multi_query`

    :param str multi_query: one or more SQL statements separated by semicolons
    :rtype: list[string]
    :return: individual SQL statements in `multi_query`
    """
    multi_query = multi_query.strip('; \n\t')  # prevent final `split(';')` from creating empty strings
    return multi_query.split(';')

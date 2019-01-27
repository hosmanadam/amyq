def break_up_query(multi_query):
    """
    Return list of individual SQL statements in `multi_query`

    :param str multi_query: one or more SQL statements separated by semicolons
    :rtype: list[string]
    :return: individual SQL statements in `multi_query`
    """
    multi_query = multi_query.strip('; \n\t')  # prevent final `split(';')` from creating empty strings
    return multi_query.split(';')


def paginate(questions, page_number, questions_per_page):
    if page_number == 'all':
        return questions
    elif page_number.isnumeric():
        first = (int(page_number) - 1) * questions_per_page
        return questions[first:first + questions_per_page]
    else:
        return None

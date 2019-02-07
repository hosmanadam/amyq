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


def prettify_user_info(user_info):
    user_info['full_name'] = f"{user_info.get('first_name')} {user_info.get('last_name')}"
    if user_info.get('locality') and user_info.get('country'):
        user_info['location'] = f"{user_info.get('locality')}, {user_info.get('country')}"
    else:
        user_info['location'] = user_info.get('locality') or user_info.get('country') or ''
    return user_info

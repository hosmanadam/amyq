from db.cnx import connection_handler
from db import queries


@connection_handler(dictionary=True)
def get_info_for_all_users(connection, cursor):
    cursor.execute(queries.read_info_for_all_users)
    return cursor.fetchall()


@connection_handler(dictionary=True)
def get_all_entries_by_user(connection, cursor, username):
    cursor.execute(queries.read_questions_by_user, params={'username': username})
    questions = cursor.fetchall()
    cursor.execute(queries.read_answers_by_user, params={'username': username})
    answers = cursor.fetchall()
    cursor.execute(queries.read_comments_by_user, params={'username': username})
    comments = cursor.fetchall()
    return questions, answers, comments


@connection_handler(dictionary=True)
def get_questions(connection, cursor, order_by, order_direction, search=''):
    cursor.execute(
        queries.read_questions_for_search,
        params={'order_by': order_by, 'order_direction': order_direction, 'search': search}
    )
    questions = cursor.fetchall()
    questions_ordered = sorted(
        questions,
        key=lambda x: x[order_by],
        reverse=(True if order_direction == 'DESC' else False)
    )
    return questions_ordered


@connection_handler(dictionary=True)
def get_question(connection, cursor, user_id, question_id):
    cursor.execute(queries.increment_question_view_count, params={'user_id': user_id, 'question_id': question_id})
    # Get question
    cursor.execute(queries.read_question, params={'id': question_id})
    question = cursor.fetchall()[0]
    # Get its tags
    cursor.execute(queries.read_tags_for_question, params={'question_id': question_id})
    tags = cursor.fetchall()
    # Get its comments
    cursor.execute(queries.read_comments_for_question, params={'question_id': question_id})
    question_comments = cursor.fetchall()
    # Get its answers with their comments
    cursor.execute(queries.read_answers, params={'question_id': question_id})
    answers = cursor.fetchall()
    for answer in answers:
        cursor.execute(queries.read_comments_for_answer, params={'answer_id': answer['id']})
        answer_comments = cursor.fetchall()
        answer.update({'comments': answer_comments})
    # Merge all into question
    question.update({'tags': tags, 'comments': question_comments, 'answers': answers})
    return question


@connection_handler(dictionary=True)
def get_answer(connection, cursor, answer_id):
    cursor.execute(queries.read_answer, params={'id': answer_id})
    answer = cursor.fetchall()[0]
    return answer


@connection_handler(dictionary=True)
def get_comment(connection, cursor, comment_id):
    cursor.execute(queries.read_comment, params={'id': comment_id})
    comment = cursor.fetchall()[0]
    return comment


@connection_handler(dictionary=True)
def get_existing_tags(connection, cursor):
    cursor.execute(queries.read_existing_tags)
    existing_tags = cursor.fetchall()
    return existing_tags


@connection_handler(dictionary=True)
def get_latest_content_match_id(connection, cursor, form):
    title = form['title']
    cursor.execute(queries.read_latest_content_match_id, params={'title': title})
    question_id = cursor.fetchall()[0]['id']
    return question_id


@connection_handler(dictionary=True)
def get_user_info(connection, cursor, username):
    cursor.execute(queries.read_user_info_for_username, params={'username': username})
    user_info = cursor.fetchall()[0]
    user_info['password_hash'] = bytes(user_info['password_hash'])
    return user_info


# TODO: test
@connection_handler(dictionary=True)
def get_user_reputation(connection, cursor, user_id):
    cursor.execute(queries.read_user_reputation, params={'user_id': user_id})
    query_result = cursor.fetchall()[0]
    return sum(query_result.values())


@connection_handler(dictionary=True)
def get_question_id_for_answer_id(connection, cursor, answer_id):
    cursor.execute(queries.read_question_id_for_answer_id, params={'id': answer_id})
    question_id = cursor.fetchall()[0]['question_id']
    return question_id


@connection_handler(dictionary=True)
def get_question_id_for_comment_id(connection, cursor, comment_id):
    cursor.execute(queries.read_comment, params={'id': comment_id})
    comment = cursor.fetchall()[0]
    question_id, answer_id = comment.get('question_id'), comment.get('answer_id')
    if question_id:
        return question_id
    else:
        return get_question_id_for_answer_id(answer_id)


@connection_handler(dictionary=True)
def add_question(connection, cursor, form, user_id):
    title = form['title']
    body = form['body'] or None
    image_url = form['image_url'] or None
    cursor.execute(queries.add_question, params={'user_id': user_id, 'title': title, 'body': body, 'image_url': image_url})


@connection_handler(dictionary=True)
def add_existing_tag_to_question(connection, cursor, user_id, question_id, tag_id):
    cursor.execute(queries.add_existing_tag_to_question, params={'user_id': user_id, 'question_id': question_id, 'tag_id': tag_id})


@connection_handler(dictionary=True)
def add_new_tag_to_question(connection, cursor, user_id, question_id, tag_name):
    cursor.execute(queries.add_new_tag, params={'user_id': user_id, 'name': tag_name})
    cursor.execute(queries.read_tag_id_for_tag_name, params={'name': tag_name})
    tag_id = cursor.fetchall()[0]['id']
    add_existing_tag_to_question(connection, cursor, question_id, tag_id)


@connection_handler(dictionary=True)
def add_answer(connection, cursor, form, user_id, question_id):
    body = form['body']
    image_url = form['image_url'] or None
    cursor.execute(queries.add_answer, params={'user_id': user_id, 'question_id': question_id, 'body': body, 'image_url': image_url})


@connection_handler(dictionary=True)
def add_question_comment(connection, cursor, form, user_id, question_id):
    body = form['body']
    cursor.execute(queries.add_question_comment, params={'user_id': user_id, 'question_id': question_id, 'body': body})


@connection_handler(dictionary=True)
def add_answer_comment(connection, cursor, form, user_id, answer_id):
    body = form['body']
    cursor.execute(queries.add_answer_comment, params={'user_id': user_id, 'answer_id': answer_id, 'body': body})


@connection_handler(dictionary=True)
def add_user(
    connection,
    cursor,
    username,
    password_hash,
    email,
    first_name,
    last_name,
    locality,
    country,
    facebook_username,
    github_username,
    twitter_username,
    linkedin_profile_url,
):
    cursor.execute(queries.add_user, params={
        'username': username,
        'password_hash': password_hash,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'locality': locality or None,
        'country': country or None,
        'facebook_username': facebook_username or None,
        'github_username': github_username or None,
        'twitter_username': twitter_username or None,
        'linkedin_profile_url': linkedin_profile_url or None,
    })


@connection_handler(dictionary=True)
def update_question(connection, cursor, form, question_id):
    title = form['title']
    body = form['body'] or None
    image_url = form['image_url'] or None
    cursor.execute(queries.update_question, params={'title': title, 'body': body, 'image_url': image_url, 'id': question_id})


@connection_handler(dictionary=True)
def update_answer(connection, cursor, form, answer_id):
    body = form['body']
    image_url = form['image_url'] or None
    cursor.execute(queries.update_answer, params={'body': body, 'image_url': image_url, 'id': answer_id})


@connection_handler(dictionary=True)
def update_comment(connection, cursor, form, comment_id):
    body = form['body']
    cursor.execute(queries.update_comment, params={'body': body, 'id': comment_id})


@connection_handler(dictionary=True)
def update_question_vote_count(connection, cursor, direction, user_id, question_id):
    value = 1 if direction == 'up' else -1
    cursor.execute(queries.update_question_vote_count, params={'user_id': user_id, 'value': value, 'question_id': question_id})


@connection_handler(dictionary=True)
def update_answer_vote_count(connection, cursor, direction, user_id, answer_id):
    value = 1 if direction == 'up' else -1
    cursor.execute(queries.update_answer_vote_count, params={'user_id': user_id, 'value': value, 'answer_id': answer_id})


@connection_handler(dictionary=True)
def accept_answer(connection, cursor, question_id, answer_id):
    cursor.execute(queries.update_accepted_answer, params={'id': question_id, 'answer_id': answer_id})


@connection_handler(dictionary=True)
def unaccept_answer(connection, cursor, question_id, answer_id):
    cursor.execute(queries.update_accepted_answer, params={'id': question_id, 'answer_id': None})


@connection_handler(dictionary=True)
def delete_question(connection, cursor, question_id):
    cursor.execute(queries.delete_question, params={'id': question_id})


@connection_handler(dictionary=True)
def delete_tag_from_question(connection, cursor, question_id, tag_id):
    cursor.execute(queries.delete_tag_from_question, params={'question_id': question_id, 'tag_id': tag_id})


@connection_handler(dictionary=True)
def delete_answer(connection, cursor, answer_id):
    cursor.execute(queries.delete_answer, params={'id': answer_id})


@connection_handler(dictionary=True)
def delete_comment(connection, cursor, comment_id):
    cursor.execute(queries.delete_comment, params={'id': comment_id})

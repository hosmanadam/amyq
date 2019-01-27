from db.cnx import connection_handler
from db import queries


@connection_handler(dictionary=True)
def get_questions(connection, cursor, order_by, order_direction, search):
    if search:
        cursor.execute(
            queries.read_questions_for_search,
            params={'order_by': order_by, 'order_direction': order_direction, 'search': search}
        )
    else:
        cursor.execute(queries.read_questions, params={'order_by': order_by, 'order_direction': order_direction})
    questions = cursor.fetchall()
    questions_ordered = sorted(
        questions,
        key=lambda x: x[order_by],
        reverse=(True if order_direction == 'DESC' else False)
    )
    return questions_ordered


@connection_handler(dictionary=True)
def get_question(connection, cursor, question_id):
    cursor.execute(queries.read_question, params={'id': question_id})
    question = cursor.fetchall()[0]
    cursor.execute(queries.read_comments_for_question, params={'question_id': question_id})
    comments = cursor.fetchall()
    question.update({'comments': comments})
    return question


@connection_handler(dictionary=True)
def get_answers(connection, cursor, question_id):
    cursor.execute(queries.read_answers, params={'id': question_id})
    answers = cursor.fetchall()
    for answer in answers:
        cursor.execute(queries.read_comments_for_answer, params={'answer_id': answer['id']})
        comments = cursor.fetchall()
        answer.update({'comments': comments})
    return answers


@connection_handler(dictionary=True)
def get_answer(connection, cursor, answer_id):
    cursor.execute(queries.read_answer, params={'id': answer_id})
    answer = cursor.fetchall()[0]
    return answer


@connection_handler(dictionary=True)
def add_question(connection, cursor, form):
    title = form['title']
    body = form['body'] or None
    image_url = form['image_url'] or None
    cursor.execute(queries.add_question, params={'title': title, 'body': body, 'image_url': image_url})


@connection_handler(dictionary=True)
def update_question(connection, cursor, form, question_id):
    title = form['title']
    body = form['body'] or None
    image_url = form['image_url'] or None
    cursor.execute(queries.update_question, params={'title': title, 'body': body, 'image_url': image_url, 'id': question_id})


@connection_handler(dictionary=True)
def update_answer(connection, cursor, form, answer_id):
    body = form['body'] or None
    image_url = form['image_url'] or None
    cursor.execute(queries.update_answer, params={'body': body, 'image_url': image_url, 'id': answer_id})


@connection_handler(dictionary=True)
def add_answer(connection, cursor, form, question_id):
    body = form['body']
    image_url = form['image_url'] or None
    cursor.execute(queries.add_answer, params={'question_id': question_id, 'body': body, 'image_url': image_url})


@connection_handler(dictionary=True)
def get_latest_content_match_id(connection, cursor, form):
    title = form['title']
    cursor.execute(queries.read_latest_content_match_id, params={'title': title})
    question_id = cursor.fetchall()[0]['id']
    return question_id


@connection_handler(dictionary=True)
def update_question_vote_count(connection, cursor, direction, id_):
    value = 1 if direction == 'up' else -1
    cursor.execute(queries.update_question_vote_count, params={'value': value, 'id': id_})


@connection_handler(dictionary=True)
def update_answer_vote_count(connection, cursor, direction, id_):
    value = 1 if direction == 'up' else -1
    cursor.execute(queries.update_answer_vote_count, params={'value': value, 'id': id_})


@connection_handler(dictionary=True)
def get_question_id_for_answer_id(connection, cursor, answer_id):
    cursor.execute(queries.read_question_id_for_answer_id, params={'id': answer_id})
    question_id = cursor.fetchall()[0]['question_id']
    return question_id


@connection_handler(dictionary=True)
def delete_question(connection, cursor, question_id):
    cursor.execute(queries.delete_question, params={'id': question_id})


@connection_handler(dictionary=True)
def delete_answer(connection, cursor, answer_id):
    cursor.execute(queries.delete_answer, params={'id': answer_id})


@connection_handler(dictionary=True)
def add_question_comment(connection, cursor, form, question_id):
    body = form['body']
    cursor.execute(queries.add_question_comment, params={'question_id': question_id, 'body': body})


@connection_handler(dictionary=True)
def add_answer_comment(connection, cursor, form, answer_id):
    body = form['body']
    cursor.execute(queries.add_answer_comment, params={'answer_id': answer_id, 'body': body})

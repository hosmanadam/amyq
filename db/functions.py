from cnx import connection_handler
from db import queries


@connection_handler(dictionary=True)
def get_questions(connection, cursor, order_by='time_submitted', order_direction='DESC'):
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
    return question


@connection_handler(dictionary=True)
def get_answers(connection, cursor, question_id):
    cursor.execute(queries.read_answers, params={'id': question_id})
    answers = cursor.fetchall()
    return answers


@connection_handler(dictionary=True)
def add_question(connection, cursor, form):
    title = form['title']
    body = form['body'] or None
    image_url = form['image_url'] or None
    cursor.execute(queries.add_question, params={'title': title, 'body': body, 'image_url': image_url})


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

from cnx import connection_handler
from db import queries


@connection_handler(dictionary=True)
def get_questions(connection, cursor):
    cursor.execute(queries.read_questions)
    questions = cursor.fetchall()
    return questions


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
def get_latest_content_match_id(connection, cursor, form):
    title = form['title']
    cursor.execute(queries.read_latest_content_match_id, params={'title': title})
    question_id = cursor.fetchall()[0]['id']
    return question_id

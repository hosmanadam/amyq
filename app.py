import math
import os

from flask import (
    Flask,
    render_template,
    redirect,
    request,
    session,
)

import auth
from db import db_handler
from util import paginate, prettify_user_info

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route('/')
@app.route('/questions/')
def index():
    return redirect('/questions/1')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        source_url = request.form.get('source_url')
        user_info = auth.login(username, password)
        if user_info:
            session.update(user_info)
            return redirect(source_url or '/questions/1')
        else:
            return render_template('login.html', message='Incorrect username or password.', source_url=source_url)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/questions/1')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        auth.register(request.form)
        return redirect('/login')


@app.route('/user/<username>')
@auth.needs_login(session)
def user(username):
    user = db_handler.get_user_info(username)
    user.update(db_handler.get_user_reputation(user.get('id')))
    user = prettify_user_info(user)
    questions, answers, comments = db_handler.get_all_entries_by_user(username)
    return render_template('user.html', user=user, questions=questions, answers=answers, comments=comments)


@app.route('/users')
@auth.needs_login(session)
def users():
    users = db_handler.get_info_for_all_users()
    for user in users:
        user = prettify_user_info(user)
    return render_template('users.html', users=users)


@app.route('/questions/<page_number>')
def questions(page_number):
    if request.args.get('ordering'):
        order_by, order_direction = request.args.get('ordering').split('-')
    else:
        order_by, order_direction = 'created', 'DESC'
    text_search = request.args.get('text_search') or ''
    tag_search = request.args.get('tag_choice_id') or ''
    if request.args.get('questions_per_page'):
        questions_per_page = int(request.args.get('questions_per_page'))
    else:
        questions_per_page = 5
    questions = db_handler.get_questions(order_by=order_by, order_direction=order_direction, text_search=text_search, tag_search=tag_search)
    page_numbers = range(1, math.ceil(len(questions)/questions_per_page) + 1)
    questions = paginate(questions, page_number, questions_per_page)
    existing_tags = db_handler.get_existing_tags()
    return render_template(
        'questions.html',
        questions=questions,
        ordering=request.args.get('ordering') or 'created-DESC',
        text_search=text_search,
        tag_search=tag_search,
        page_number=int(page_number),
        page_numbers=page_numbers,
        questions_per_page=questions_per_page,
        query_string=request.query_string.decode("utf-8"),
        existing_tags=existing_tags,
    )


@app.route('/question/<int:question_id>/')
@auth.needs_login(session)
def question(question_id):
    question = db_handler.get_question(session.get('id'), question_id)
    return render_template('question.html', question=question, session=session)


@app.route('/tags/')
def tags():
    tags = db_handler.get_tags_with_question_count()
    return render_template('tags.html', tags=tags)


@app.route('/add-question', methods=['GET', 'POST'])
@auth.needs_login(session)
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html', questions=questions)
    if request.method == 'POST':
        db_handler.add_question(request.form, session.get('id'))
        question_id = db_handler.get_latest_content_match_id(request.form)
        return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/add-tag', methods=['GET', 'POST'])
@auth.needs_login(session)
def add_tag_to_question(question_id):
    if request.method == 'GET':
        question = db_handler.get_question(session.get('id'), question_id)
        existing_tags = db_handler.get_existing_tags()
        other_tags = [tag for tag in existing_tags if tag not in question.get('tags')]
        return render_template('add-tag.html', question=question, other_tags=other_tags)
    if request.method == 'POST':
        if request.form.get('new_tag_name'):
            tag_name = request.form.get('new_tag_name')
            db_handler.add_new_tag_to_question(session.get('id'), question_id, tag_name)
            return redirect(f'/question/{question_id}')
        if request.form.get('tag_choice_id'):
            tag_id = int(request.form.get('tag_choice_id'))
            db_handler.add_existing_tag_to_question(session.get('id'), question_id, tag_id)
            return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/add-comment', methods=['GET', 'POST'])
@auth.needs_login(session)
def add_question_comment(question_id):
    if request.method == 'GET':
        question = db_handler.get_question(session.get('id'), question_id)
        return render_template('add-comment.html', question=question)
    if request.method == 'POST':
        db_handler.add_question_comment(request.form, session.get('id'), question_id)
        return redirect(f'/question/{question_id}')


@app.route('/answer/<int:answer_id>/add-comment', methods=['GET', 'POST'])
@auth.needs_login(session)
def add_answer_comment(answer_id):
    if request.method == 'GET':
        answer = db_handler.get_answer(answer_id)
        return render_template('add-comment.html', answer=answer)
    if request.method == 'POST':
        db_handler.add_answer_comment(request.form, session.get('id'), answer_id)
        question_id = db_handler.get_question_id_for_answer_id(answer_id)
        return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
@auth.needs_login(session)
def edit_question(question_id):
    if request.method == 'GET':
        question = db_handler.get_question(session.get('id'), question_id)
        return render_template('edit-question.html', question=question)
    if request.method == 'POST':
        db_handler.update_question(request.form, question_id)
        return redirect(f'/question/{question_id}')


@app.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])
@auth.needs_login(session)
def edit_answer(answer_id):
    if request.method == 'GET':
        answer = db_handler.get_answer(answer_id)
        return render_template('edit-answer.html', answer=answer)
    if request.method == 'POST':
        db_handler.update_answer(request.form, answer_id)
        question_id = db_handler.get_question_id_for_answer_id(answer_id)
        return redirect(f'/question/{question_id}')


@app.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
@auth.needs_login(session)
def edit_comment(comment_id):
    if request.method == 'GET':
        comment = db_handler.get_comment(comment_id)
        return render_template('edit-comment.html', comment=comment)
    if request.method == 'POST':
        db_handler.update_comment(request.form, comment_id)
        question_id = db_handler.get_question_id_for_comment_id(comment_id)
        return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/vote-<direction>', methods=['POST'])
@auth.needs_login(session)
def vote_on_question(question_id, direction):
    db_handler.update_question_vote_count(direction, session.get('id'), question_id)
    return redirect(f'/question/{question_id}')


@app.route('/answer/<int:answer_id>/vote-<direction>', methods=['POST'])
@auth.needs_login(session)
def vote_on_answer(answer_id, direction):
    db_handler.update_answer_vote_count(direction, session.get('id'), answer_id)
    question_id = db_handler.get_question_id_for_answer_id(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/accept-answer/<int:answer_id>/', methods=['POST'])
@auth.needs_login(session)
def accept_answer(question_id, answer_id):
    db_handler.accept_answer(question_id, answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/unaccept-answer/<int:answer_id>/', methods=['POST'])
@auth.needs_login(session)
def unaccept_answer(question_id, answer_id):
    db_handler.unaccept_answer(question_id, answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/submit-answer', methods=['POST'])
@auth.needs_login(session)
def submit_answer(question_id):
    db_handler.add_answer(request.form, session.get('id'), question_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/delete')
@auth.needs_login(session)
def delete_question(question_id):
    db_handler.delete_question(question_id)
    return redirect(f'/questions')


@app.route('/question/<int:question_id>/tag/<int:tag_id>/delete')
@auth.needs_login(session)
def delete_tag_from_question(question_id, tag_id):
    db_handler.delete_tag_from_question(question_id, tag_id)
    return redirect(f'/question/{question_id}')


@app.route('/answer/<int:answer_id>/delete')
@auth.needs_login(session)
def delete_answer(answer_id):
    question_id = db_handler.get_question_id_for_answer_id(answer_id)
    db_handler.delete_answer(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/comment/<int:comment_id>/delete')
@auth.needs_login(session)
def delete_comment(comment_id):
    question_id = db_handler.get_question_id_for_comment_id(comment_id)
    db_handler.delete_comment(comment_id)
    return redirect(f'/question/{question_id}')


if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000,
    )

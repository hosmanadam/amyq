import math
import os

from flask import (
    abort,
    Flask,
    render_template,
    redirect,
    request,
)

from db import db_handler
from util import paginate

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route('/')
@app.route('/questions')
@app.route('/questions/')
def index():
    return redirect('/questions/1')


@app.route('/questions/<page_number>', methods=['GET', 'POST'])
def questions(page_number):
    if request.form.get('ordering'):
        order_by, order_direction = request.form.get('ordering').split('-')
    else:
        order_by, order_direction = 'time_submitted', 'DESC'
    search = request.form.get('search')
    if request.form.get('questions_per_page'):
        questions_per_page = int(request.form.get('questions_per_page'))
    else:
        questions_per_page = 5
    questions = db_handler.get_questions(order_by=order_by, order_direction=order_direction, search=search)
    page_numbers = range(1, math.ceil(len(questions)/questions_per_page) + 1)
    questions = paginate(questions, page_number, questions_per_page) or abort(404)
    return render_template(
        'questions.html',
        questions=questions,
        ordering=request.form.get('ordering'),
        search=search,
        page_number=int(page_number),
        page_numbers=page_numbers,
        questions_per_page=questions_per_page,
    )


@app.route('/question/<int:question_id>')
def question(question_id):
    question = db_handler.get_question(question_id, increment_view_count=True)
    return render_template('question.html', question=question)


@app.route('/add-question')
def add_question():
    return render_template('add-question.html', questions=questions)


@app.route('/question/<int:question_id>/add-comment')
def add_question_comment(question_id):
    question = db_handler.get_question(question_id)
    return render_template('add-comment.html', question=question)


@app.route('/answer/<int:answer_id>/add-comment')
def add_answer_comment(answer_id):
    answer = db_handler.get_answer(answer_id)
    return render_template('add-comment.html', answer=answer)


@app.route('/question/<int:question_id>/edit')
def edit_question(question_id):
    question = db_handler.get_question(question_id)
    return render_template('edit-question.html', question=question)


@app.route('/answer/<int:answer_id>/edit')
def edit_answer(answer_id):
    answer = db_handler.get_answer(answer_id)
    return render_template('edit-answer.html', answer=answer)


@app.route('/comment/<int:comment_id>/edit')
def edit_comment(comment_id):
    comment = db_handler.get_comment(comment_id)
    return render_template('edit-comment.html', comment=comment)


@app.route('/question/<int:question_id>/vote-<direction>', methods=['POST'])
def vote_on_question(question_id, direction):
    db_handler.update_question_vote_count(direction=direction, id_=question_id)
    return redirect(f'/question/{question_id}')


@app.route('/answer/<int:answer_id>/vote-<direction>', methods=['POST'])
def vote_on_answer(answer_id, direction):
    db_handler.update_answer_vote_count(direction=direction, id_=answer_id)
    question_id = db_handler.get_question_id_for_answer_id(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/submit-question', methods=['POST'])
def submit_question():
    db_handler.add_question(request.form)
    question_id = db_handler.get_latest_content_match_id(request.form)
    return redirect(f'/question/{question_id}')


@app.route('/submit-answer/<int:question_id>', methods=['POST'])
def submit_answer(question_id):
    db_handler.add_answer(request.form, question_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/submit-comment', methods=['POST'])
def submit_question_comment(question_id):
    db_handler.add_question_comment(request.form, question_id)
    return redirect(f'/question/{question_id}')


@app.route('/answer/<int:answer_id>/submit-comment', methods=['POST'])
def submit_answer_comment(answer_id):
    db_handler.add_answer_comment(request.form, answer_id)
    question_id = db_handler.get_question_id_for_answer_id(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/submit-edited-question', methods=['POST'])
def submit_edited_question(question_id):
    db_handler.update_question(request.form, question_id)
    return redirect(f'/question/{question_id}')


@app.route('/answer/<int:answer_id>/submit-edited-answer', methods=['POST'])
def submit_edited_answer(answer_id):
    db_handler.update_answer(request.form, answer_id)
    question_id = db_handler.get_question_id_for_answer_id(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/comment/<int:comment_id>/submit-edited-comment', methods=['POST'])
def submit_edited_comment(comment_id):
    db_handler.update_comment(request.form, comment_id)
    question_id = db_handler.get_question_id_for_comment_id(comment_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/delete')
def delete_question(question_id):
    db_handler.delete_question(question_id)
    return redirect(f'/questions')


@app.route('/answer/<int:answer_id>/delete')
def delete_answer(answer_id):
    question_id = db_handler.get_question_id_for_answer_id(answer_id)
    db_handler.delete_answer(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/comment/<int:comment_id>/delete')
def delete_comment(comment_id):
    question_id = db_handler.get_question_id_for_comment_id(comment_id)
    db_handler.delete_comment(comment_id)
    return redirect(f'/question/{question_id}')


if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000,
    )

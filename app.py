import os

from flask import (
    Flask,
    render_template,
    redirect,
    request,
)

import db.functions as dbfunc

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route('/')
def index():
    return redirect('/questions')


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST' and request.form['ordering']:
        order_by, order_direction = request.form['ordering'].split('-')
        questions = dbfunc.get_questions(order_by=order_by, order_direction=order_direction)
        return render_template('questions.html', questions=questions, ordering=request.form['ordering'])
    else:
        questions = dbfunc.get_questions()
        return render_template('questions.html', questions=questions, ordering='time_submitted-DESC')


@app.route('/add-question')
def add_question():
    return render_template('add-question.html', questions=questions)


@app.route('/question/<int:question_id>/edit')
def edit_question(question_id):
    question = dbfunc.get_question(question_id)
    return render_template('edit-question.html', question=question)


@app.route('/question/<int:question_id>/submit-edited-question', methods=['POST'])
def submit_edited_question(question_id):
    dbfunc.update_question(request.form, question_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/vote-<direction>', methods=['POST'])
def vote_on_question(question_id, direction):
    dbfunc.update_question_vote_count(direction=direction, id_=question_id)
    return redirect(f'/question/{question_id}')


@app.route('/answer/<int:answer_id>/vote-<direction>', methods=['POST'])
def vote_on_answer(answer_id, direction):
    dbfunc.update_answer_vote_count(direction=direction, id_=answer_id)
    question_id = dbfunc.get_question_id_for_answer_id(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/submit-question', methods=['POST'])
def submit_question():
    dbfunc.add_question(request.form)
    question_id = dbfunc.get_latest_content_match_id(request.form)
    return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/delete')
def delete_question(question_id):
    dbfunc.delete_question(question_id)
    return redirect(f'/questions')


@app.route('/answer/<int:answer_id>/delete')
def delete_answer(answer_id):
    question_id = dbfunc.get_question_id_for_answer_id(answer_id)
    dbfunc.delete_answer(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/submit-answer/<int:question_id>', methods=['POST'])
def submit_answer(question_id):
    dbfunc.add_answer(request.form, question_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>')
def question(question_id):
    question = dbfunc.get_question(question_id)
    answers = dbfunc.get_answers(question_id)
    return render_template('question.html', question=question, answers=answers)


if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000,
    )

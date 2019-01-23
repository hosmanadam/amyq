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


@app.route('/questions')
def questions():
    questions = dbfunc.get_questions()
    return render_template('questions.html', questions=questions)


@app.route('/add-question')
def add_question():
    return render_template('add-question.html', questions=questions)


@app.route('/submit-question', methods=['POST'])
def submit_question():
    dbfunc.add_question(request.form)
    question_id = dbfunc.get_latest_content_match_id(request.form)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>')
def question(question_id):
    question = dbfunc.get_question(question_id)
    answers = dbfunc.get_answers(question_id)
    return render_template('question.html', question=question, answers=answers)


if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000,
    )

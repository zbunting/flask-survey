from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get('/')
def index():
    """Renders the main survey page"""
    # TODO: change name of survey and add instructions
    return render_template("survey_start.jinja")


@app.post('/begin')
def redirect_to_questions():
    """Redirect to the questions page"""

    return redirect("/questions/0")


@app.get('/questions/<int:question_num>')
def generate_questions(question_num):
    """Generates page for specific question """
    question = survey.questions[question_num]

    return render_template('question.jinja', question=question)

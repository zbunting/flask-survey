from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get('/')
def index():  # verb noun function show_home
    """Renders the main survey page"""

    return render_template("survey_start.jinja", survey=survey)


@app.post('/begin')
def redirect_to_questions():  # bit too specific start_survey
    """Redirect to the questions page"""

    return redirect("/questions/0")


@app.get('/questions/<int:question_num>')
def generate_questions(question_num):  # display maybe instead of generate
    """Generates page for specific question. Redirect to thankyou
    if questions complete"""

    # TODO: change if you go to further question
    if question_num >= len(survey.questions):
        return redirect('/thankyou')

    question = survey.questions[question_num]

    return render_template(
        'question.jinja',
        question=question,
        question_num=question_num
    )


# in theory, could go to answer /answer/99 for example
@app.post('/answer/<int:question_num>')
def handle_answer(question_num):  # TODO: refactor using session dict
    """Store answer and redirect to next questions in survey"""

    next_question_num = str(question_num + 1)
    answer = request.form.get("answer")

    responses.append(answer)

    return redirect(f"/questions/{next_question_num}")


@app.get('/thankyou')
def show_reponses():
    """Generates thank you page for user with list of
    questions and answers"""

    questions_num = len(survey.questions)
    return render_template(
        "completion.jinja",
        responses=responses,
        questions_num=questions_num,
        questions=survey.questions
    )

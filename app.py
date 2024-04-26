from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# Good idea to include, helps VS code to help us if we misspell, updatein one spot
RESPONSE_KEY = 'responses'


@app.get('/')
def index():  # verb noun function show_home
    """Renders the main survey page"""

    return render_template("survey_start.jinja", survey=survey)


@app.post('/begin')
def redirect_to_questions():  # bit too specific start_survey
    """Redirect to the questions page"""

    session["responses"] = []

    return redirect("/questions/0")


@app.get('/questions/<int:question_num>')
def generate_questions(question_num):  # display maybe instead of generate
    """Generates page for specific question. Redirect to thankyou
    if questions complete"""

    questions_answered = len(session["responses"])

    if question_num > questions_answered:
        flash("DON'T TRY TO SKIP AHEAD!")
        return redirect(f"/questions/{str(questions_answered)}")

    elif questions_answered >= len(survey.questions):
        return redirect("/thankyou")

    question = survey.questions[question_num]

    return render_template(
        'question.jinja',
        question=question,
        question_num=question_num
    )


@app.post('/answer')
def handle_answer():
    """Store answer and redirect to next questions in survey"""

    answer = request.form.get("answer")
    new_responses_list = session["responses"].append(answer)
    breakpoint()
    session["response"] = new_responses_list # TODO: worked by accident - need to pull out responses, change it, then reassign it

    next_question_num = str(len(session["responses"]))

    return redirect(f"/questions/{next_question_num}")


@app.get('/thankyou')
def show_reponses():
    """Generates thank you page for user with list of
    questions and answers"""

    questions_num = len(survey.questions)
    return render_template(
        "completion.jinja",
        responses=session["responses"],
        questions_num=questions_num,
        questions=survey.questions
    )

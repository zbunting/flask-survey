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

    return render_template("survey_start.jinja")

@app.post('/begin')
def redirect_to_questions():
    """Redirect to the questions page"""

    return redirect("/questions")


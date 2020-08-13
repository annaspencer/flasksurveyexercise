from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app =Flask(__name__)

app.config['SECRET_KEY'] = "129-533-556"
debug = DebugToolbarExtension(app) 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True



RESPONSES = "responses"

@app.route('/')
def start_page():
    """ homepage"""
   
    return render_template("startpage.html", survey=survey)

@app.route("/start", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES] = []

    return redirect("/questions/0")



@app.route('/questions/<int:qid>')
def start_questions(qid):
    """questions"""
    responses = session.get(RESPONSES)

    if (responses is None):
        # this isn't working...
        return redirect("/start")
    if (len(responses) == len(survey.questions)):
        return redirect("/thankyou")

    if (len(responses) != qid):
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]

   
    return render_template("questions.html", survey = survey, question =question)

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    choice = request.form['answer']
    responses = session[RESPONSES]
    responses.append(choice)
    session[RESPONSES] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/thankyou")

    else:
        return redirect(f"/questions/{len(responses)}")





@app.route("/thankyou")
def complete():
    """Survey complete. Show completion page."""

    return render_template("thankyou.html")
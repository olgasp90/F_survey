from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_secret_password'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def home():
    """select survey"""
    TITLE = satisfaction_survey.title
    INSTRUCTIONS = satisfaction_survey.instructions
    return render_template('survey.html', title=TITLE, instructions=INSTRUCTIONS)


@app.route("/begin", methods=["POST"])
def start_survey():
    """redirect to the first question"""
    return redirect("/questions/0")


@app.route('/questions/<num>')
def questions(num):
    num = int(float(num))

    if (responses is None):
        return redirect('/')

    if(len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')

    if(len(responses) != num):
        flash(f'Invalid question id: {num}.')
        return redirect(f"/questions/{len(responses)}")
    question = satisfaction_survey.questions[num]
    return render_template("question.html", question_num=num, question=question)


@app.route('/answer', methods=['POST'])
def survey_answers():
    answers = request.form['answer']
    """ add the answer to the responses list"""
    responses.append(answers)
    print(responses)
    if(len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def end_survey():
    return render_template('complete.html')

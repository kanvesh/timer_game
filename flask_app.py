from flask import Flask, render_template, request, redirect, url_for, session
import json
import random
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load questions from a JSON file
with open('questions.json', 'r') as f:
    questions = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['start_time'] = time.time()
        session['score'] = 0
        session['current_question'] = random.choice(questions)  # Pick a random question and store it in session
        return redirect(url_for('question'))
    elif 'username' in session:
        # Restart the game with a new random question without asking for the name
        session['start_time'] = time.time()
        session['score'] = 0
        session['current_question'] = random.choice(questions)
        return redirect(url_for('question'))
    return render_template('home.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'username' not in session or time.time() - session['start_time'] > 60:
        return redirect(url_for('end_game'))
    if request.method == 'POST':
        user_answer = request.form['choice']
        if user_answer == session['current_question']['answer']:
            session['score'] += 1
        # Pick a new random question and store it in session
        session['current_question'] = random.choice(questions)
        return redirect(url_for('question'))
    # Continue showing questions if under 60 seconds
    return render_template('question.html', question=session['current_question'], score=session.get('score', 0))

@app.route('/end_game', methods=['GET', 'POST'])
def end_game():
    if request.method == 'POST':
        return redirect(url_for('home'))
    elapsed_time = time.time() - session['start_time']
    if elapsed_time > 60:
        session['score'] = 0
    elif 'stop' in request.args and request.args.get('stop') == 'true':
        if elapsed_time < 30:
            pass  # Keep the score as it is
        else:
            session['score'] = 0

    elapsed_time_display = int(elapsed_time)  # Convert to integer to display seconds
    return render_template('end_game.html', score=session['score'], elapsed_time=elapsed_time_display)
if __name__ == '__main__':
    app.run(debug=True)

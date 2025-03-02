from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from rapidfuzz import fuzz

import secrets
import json
import os

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

rounds = json.loads(open(f'{os.getcwd()}/rounds.json').read())

class RoundForm(FlaskForm):
    answer = StringField('answer', default='', validators=[DataRequired()], render_kw={'autofocus': True})
    submit = SubmitField('submit')

@app.route('/')
def main():
    avail = len(rounds)
    return render_template('body.html', avail=avail)

@app.route('/game/<game_id>/<int:question>', methods=['GET', 'POST'])
def game(game_id, question):

    if 'revealed' not in session:
        session['revealed'] = 0

    if 'stats' not in session:
        session['stats'] = {}

    if 'stats_string' not in session:
        session['stats_string'] = ''
    
    if session['revealed'] == 5: session['revealed'] = 0

    rnd = rounds[game_id][question - 1]
    completed = False
    correct = False
    form = RoundForm()

    if form.validate_on_submit():
        submitted_answer = form.answer.data
        stats_key = f'{game_id}_{question}'
        if stats_key not in session['stats']:
            session['stats'][stats_key] = {'guesses': [], 'correct': rnd['answer']}
        
        session['stats'][stats_key]['guesses'].append(submitted_answer)
        session.modified = True
        
        crit = fuzz.ratio(submitted_answer.lower(), rnd['answer'].lower())

        if crit > 95:
            completed = True
            session['stats_string'] += "➊➋➌➍➎"[session['revealed']]
            session['revealed'] = 5
            correct = True
        else:
            session['revealed'] += 1
            if session['revealed'] > 4:
                completed = True
                correct = False
    else:
        print(form.errors.items())

    return render_template('round.html', rnd=rnd, form=form, revealed=session['revealed'], completed=completed, game_id=game_id, question=question, correct=correct)

@app.route('/complete/<game_id>')
def complete(game_id):
    stats = []
    for i in range(1, 11):
        stats_key = f'{game_id}_{i}'
        if stats_key in session['stats']:
            stats.append(session['stats'][stats_key])
    
    return render_template('stats.html', stats=stats, stats_string=session['stats_string'], game_id=game_id)



if __name__ == '__main__':
    app.run(debug=True)

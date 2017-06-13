from . import config,model
import os

from app import app
import json
from flask import render_template,request,session,redirect,url_for
from . import model
from . import twentyquestions as game
app.secret_key = os.urandom(24)


def reset_game():
    session.clear()



@app.route('/')
def startsession():
    session['count'] = 1
    session['asked_questions'] = {}
    session['initial_questions'] = []
    session['objects_values'] = {}
    return '''<body style="
    background-color: lightblue;
    color: white;
    text-align: center;
    font-family: verdana;
    font-size: 20px;
"><a href="/index"><h1>lets GO</h1></a></body>'''


@app.route('/index',methods = ['GET'])
def index():

    if request.method == 'GET':
        if config.DISPLAY_CANDIDATES: # clean up this section somehow
            nearby_objects_values = game.get_nearby_objects_values(session['objects_values'], how_many=10)
        else:
            nearby_objects_values = None
        if not session['asked_questions'] and not session['initial_questions'] :
            question = 'begin'
            '''elif session['asked_questions']:
            return redirect('/')'''
        else :
            question,initial_questions = game.choose_question(session['initial_questions'], session['objects_values'], session['asked_questions'])
            session['initial_questions'] = initial_questions
            if question == None or session['count'] > 20:
                return redirect(url_for('guess'))
    return render_template("index.html",question = question,count = session['count'],nearby_objects_values=nearby_objects_values)

@app.route('/begin',methods = ['POST'])
def begin():
    session['initial_questions'] = game.load_initial_questions()
    session['objects_values'] = game.load_objects_values()

    return redirect(url_for('index'))

@app.route('/restart',methods = ['POST'])
def restart():
    reset_game()
    return redirect('/')

@app.route('/answer/<int:question_id>',methods = ['POST'])
def answer(question_id):
    question_id = int(question_id)
    a = request.form.getlist('answer')[0]
    if a in ['yes', 'no', 'unsure']: answer = eval('game.' + a)
    else: answer = game.unsure
    if answer != game.unsure:
        session['count'] += 1
    game.update_local_knowledgebase(session['objects_values'], session['asked_questions'], question_id, answer)
    return redirect(url_for("index"))

@app.route('/guess',methods = ['GET'])
def guess():
    chosen = game.guess(session['objects_values'])
    return render_template("guess.html",chosen=chosen)

@app.route('/guess/<int:chosen_id>', methods=['POST'])
def guess_post(chosen_id=None):
    a = request.form.getlist('answer')[0]
    if not(chosen_id):
        chosen_id=1

    if a in ['no', 'teach me']:
        return redirect(url_for('learn'))
    elif a in ['yes']:
        game.learn(session['asked_questions'], int(chosen_id))

        reset_game()

        return redirect('/')

@app.route('/learn',methods = ['GET','POST'])
def learn():
    if request.method == 'GET':
        nearby_objects = game.get_nearby_objects(session['objects_values'], how_many=20)
        return render_template("learn.html",nearby_objects=nearby_objects)
    if request.method == 'POST':
        try :
            name = request.form.getlist('name')[0]
        except IndexError:
            return redirect('/')
        if name == 'new':
            name  = request.form.getlist('new_character')[0]
        if name:
            new_object_id = game.learn_character(session['asked_questions'], name)
        else:
            new_object_id = None

        reset_game()
        # resets game data and starts a new game

        return redirect('/')
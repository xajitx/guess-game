from app import app
import json
from flask import render_template,request,redirect,url_for
from app import model
from app import twentyquestions as game


@app.route('/adddata',methods = ['GET'])
def adddata():
    return '''<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>adddata</title>
    
</head>
    
<body>
    <a href="/adddata/addquestion"><h3>Add Questions</h3></a>
    <a href="/adddata/addobject"><h3>Add Objects</h3></a>
    <a href="/adddata/data"><h3>Train New data</h3></a>
</body>
</html>'''

@app.route('/adddata/addquestion',methods = ['GET','POST'])
def addnewquestion():
    if request.method == 'GET':
        return render_template("addQuestion.html")
    elif request.method == 'POST':
        addQue = request.form.getlist('addQue')[0]
        if addQue in ['Done']:
            return redirect(url_for("adddata"))
        else :
            question = request.form.getlist('question')[0]
            if not question.strip() == '' and not model.get_question_by_text(question.strip()):
                model.add_question(question.strip())
            return redirect('/adddata/addquestion')


@app.route('/adddata/addobject',methods = ['GET','POST'])
def addnewobject():
    if request.method == 'GET':
        return render_template("addObjects.html")
    elif request.method == 'POST':
        addQue = request.form.getlist('addObj')[0]
        if addQue in ['Done']:
            return redirect(url_for("adddata"))
        else :
            object = request.form.getlist('object')[0]
            if not object.strip() == '' and not model.get_object_by_name(object.strip()):
                model.add_object(object.strip())
            return redirect('/adddata/addobject')


@app.route('/adddata/newtrain/<int:id>',methods = ['GET','POST'])
def newtrain(id):
    if request.method == 'GET':
        objects = model.get_object_by_id(int(id))
        obj_id = objects[0]
        obj_val = objects[1]

        questions = model.get_questions()
        que_dic ={}
        for i in questions:
            key = i[0]
            value = i[1]
            que_dic[key] = value
        data_dic = model.get_data_dictionary()
        return render_template("tain_new_data.html",obj_id = obj_id, obj_val=obj_val,questions=que_dic,data=data_dic)
    elif request.method == 'POST':
        que_id_list = request.form
        for que_id in que_id_list:
            answer = que_id_list[que_id]
            if answer in ['yes', 'no']:
                value = eval('game.' + answer) * game.NEW_QUESTION_SCALE  # STRONGLY weights values learned this way
                model.update_data(int(id), int(que_id), value)
        return redirect(url_for("get_new_data"))

@app.route('/adddata/data',methods = ['GET'])
def get_new_data():
    objects = model.get_objects()
    dict ={}
    for i in objects:
        key = i[0]
        value = i[1]
        dict[key] = value
    return render_template("new_data.html",data=dict)

from app import app
import json
from flask import render_template,request,redirect,url_for
from . import model
from . import twentyquestions as game


@app.route('/admin',methods = ['GET'])
def admin():
    return render_template("admin.html")

@app.route('/admin/dq',methods = ['GET','POST'])
def delete_question():
    if request.method == 'GET':
        list = model.get_questions()
        dict = {}
        for i in list:
            key = i[0]
            value = i[1]
            dict[key]=value
        question = json.dumps(dict)
        return render_template("delete_question.html",questions = dict)
    elif request.method == 'POST':
        id = request.form.getlist('ques_id')
        if len(id) >0:
            for i in id:
                model.delete_question(int(i))

        return render_template("admin.html")


@app.route('/admin/do',methods = ['GET','POST'])
def delete_object():
    if request.method == 'GET':
        objects = model.get_objects()
        dict = {}
        for i in objects:
            key = i[0]
            value = i[1]
            dict[key] = value
        object = json.dumps(dict)
        return render_template("delete_object.html", objects=dict)
    elif request.method == 'POST':
        id = request.form.getlist('obj_id')
        if len(id) > 0:
            for i in id:
                model.delete_object(int(i))

        return render_template("admin.html")

@app.route('/admin/data',methods = ['GET'])
def get_data():
    objects = model.get_objects()
    dict ={}
    for i in objects:
        key = i[0]
        value = i[1]
        dict[key] = value
    return render_template("data.html",data=dict)

#$def with (object, questions, data)
@app.route('/admin/retrain/<int:id>',methods = ['GET','POST'])
def retrain(id):
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
        return render_template("retrain.html",obj_id = obj_id, obj_val=obj_val,questions=que_dic,data=data_dic)

    elif request.method == 'POST':
        que_id_list = request.form
        for que_id in que_id_list:
            answer = que_id_list[que_id]
            if answer in ['yes', 'no']:
                value = eval('game.' + answer) * game.RETRAIN_SCALE  # STRONGLY weights values learned this way
                model.update_data(int(id), int(que_id), value)

        return redirect(url_for("get_data"))

 
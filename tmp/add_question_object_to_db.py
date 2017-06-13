from app import model as DB


#ques_file = "questions"
#obj_file= "objects"
def add_questions(ques_file):
    with open(ques_file,'r') as f:
        content = f.read().split("\n")
        for i in content:
            if not i.strip() == '' and not DB.get_question_by_text(i.strip()):
                DB.add_question(i.strip())

def object(obj_file):
    with open(obj_file,'r') as f:
        content = f.read().split("\n")
        for i in content:
            if not i.strip() == '' and not DB.get_object_by_name(i.strip()):
                DB.add_object(i.strip())


add_questions("questions")
object("object")
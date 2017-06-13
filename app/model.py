from .config import conn
c = conn.cursor()
'''done'''
def add_object(name):
    '''Adds an object with the given name to the objects table in the database.
       Also initializes weights for each question in the data table.'''

    sql = "INSERT INTO objects (name) VALUES (?)"
    object_id = c.execute(sql,[name]).lastrowid
    conn.commit()
    # initialize weights for each question in data
    questions = get_questions()
    for question in questions:
        add_data(object_id, question[0])

    return object_id

'''done'''
def add_question(question):
    '''Adds a question with the given text to the questions table in the database.
       Also initializes weights for each object in the data table.'''
    sql = "INSERT INTO questions (text) VALUES (?)"
    question_id = c.execute(sql,[question]).lastrowid
    conn.commit()
    # initialize weights for each object in data
    objects = get_objects()
    for object in objects:
        add_data(object[0], question_id)
    return question_id

'''done'''
def add_data(object_id, question_id, value=0):
    '''Inserts a weight with value=value for a specified object_id and question_id
       into data. Defaults to value=0.'''
    sql = "INSERT INTO data (object_id,question_id,value) VALUES (?,?,?)"
    c.execute(sql, [object_id,question_id,value])
    conn.commit()


'''done'''
def update_data(object_id, question_id, value):
    '''Updates the weight for a specified object_id and question_id in data with
       the specified value.'''
    sql = "UPDATE data SET value =? WHERE object_id =? AND question_id= ? "
    c.execute(sql, [value,object_id, question_id])
    conn.commit()



# def update_weights(object_id, asked_questions):

## Dictionary {question: value}
# for question in asked_questions:
# value = asked_questions[question]
# update_data(object_id, question, value)

'''done'''
def get_objects():
    '''Returns an IterBetter of all the objects in database, where each row is a Storage object.'''
    iter = list(c.execute("select * from objects").fetchall())
    return iter
'''done'''
def get_data():
    '''Returns an IterBetter of all the data in the database, where each row is a Storage object.'''
    iter = list(c.execute("select * from data").fetchall())
    return iter

'''done'''
def get_questions():
    '''Returns an IterBetter of all the quesitons in the database, where each row is a Storage object.'''
    iter = list(c.execute("select * from questions").fetchall())
    return iter

'''done'''
def get_value(object_id, question_id):
    '''Returns the weight for given object_id question_id from data. If the weight
       does not exist, returns None.'''


    try:
        sql = "select value from data  WHERE object_id =? AND question_id= ? "
        val=list(c.execute(sql, [object_id, question_id]))[0][0]
        return val
    except IndexError:
        return None

'''done'''
def get_object_by_name(name):
    '''Returns a Storage object containing an object where name=name.'''
    try:
        sql = "select * from objects  WHERE name= ? "
        val = list(c.execute(sql, [name]))[0]
        return val
    except IndexError:
        return None

'''done'''
def get_object_by_id(id):
    '''Returns a Storage object containing an object where id=id.'''
    try:
        sql = "select * from objects  WHERE id= ? "
        val = list(c.execute(sql, [id]))[0]
        return val
    except IndexError:
        return None

'''done'''
def get_question_by_id(id):
    '''Returns a Storage object containing a question where id=id.'''
    try:
        sql = "select * from questions WHERE id= ? "
        val = list(c.execute(sql, [id]))[0]
        return val
    except IndexError:
        return None

'''done'''
def get_question_by_text(text):
    '''Returns Storage object containing a question where text=text.'''
    try:
        sql = "select * from questions WHERE text= ? "
        val = list(c.execute(sql, [text]))[0]
        return val
    except IndexError:
        return None

'''done need yto check the answer again'''
def get_data_by_question_id(question_id):
    '''Returns an IterBetter all weights for a particular question_id, where each
       row is a Storage object.'''
    try:
        sql = "select * from data WHERE question_id= ? "
        val = list(c.execute(sql, [question_id]))
        return val
    except IndexError:
        return None

'''done'''
def get_data_by_object_id(object_id):
    '''Returns an IterBetter of all weights for a particular object_id, where each
       row is a Storage object.'''
    try:
        sql = "select * from data WHERE object_id= ? "
        val = list(c.execute(sql, [object_id]))[0]
        return val
    except IndexError:
        return None

'''done'''
def get_data_dictionary():
    '''Returns the data as a dictionary object, where keys are (object_id, question_id)
       tuples, and values are the weights for that pair.'''

    d = get_data()
    data = {}

    for row in d:
        data[(row[0], row[1])] = row[2]

    return data

''''????'''
def get_num_unknowns(object_tuple, question_id):
    '''Returns the number of objects in the object_tuple where the value for the
       given question_id is zero, or unknown.'''

    assert type(object_tuple) == tuple


    try:
        sql = "SELECT count(*) FROM data where object_id IN %s AND question_id=? AND value =0" % str(
            object_tuple).replace(',)', ')')
        rows = list(c.execute(sql, [ question_id]))
        return rows[0][0]
    except IndexError:
        return 0

''''????'''
def get_num_positives(object_tuple, question_id):
    '''Returns the number of objects in the object_tuple where the value for the
       given question_id is positive.'''

    assert type(object_tuple) == tuple
    try:
        #tpl =(4, 5, 6, 7, 9, 12, 13, 14, 15, 18, 19, 20, 21, 22, 23, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 72, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244)
        sql ="SELECT count(*) FROM data where object_id IN %s AND question_id=? AND value >0" % str(object_tuple).replace(',)',')')
        rows = list(c.execute(sql,[question_id]))
        return rows[0][0]
    except IndexError:
        return 0

''''????'''
def get_num_negatives(object_tuple, question_id):
    '''Returns the number of objects in the object_tuple where the value for the
       given question_id is negative.'''

    assert type(object_tuple) == tuple


    try:
        sql = "SELECT count(*) FROM data where object_id IN %s AND question_id=? AND value <0" % str(
            object_tuple).replace(',)', ')')
        rows = list(c.execute(sql, [question_id]))
        return rows[0][0]
    except IndexError:
        return 0


def delete_question(question_id):
    '''Deletes a question and its weights for a particular question_id.
    db.delete('questions', where='id=$question_id', vars=locals())
    db.delete('data', where='question_id=$question_id', vars=locals())'''


    sql1 = "delete from questions where id = ?"
    sql2 = "delete from data where question_id=?"
    c.execute(sql1,[question_id])
    c.execute(sql1, [question_id])
    conn.commit()


def delete_object(object_id):
    '''Deletes an object and its weights for a particular object_id.'''
    sql1 = "delete from objects where id = ?"
    sql2 = "delete from data where question_id=?"
    c.execute(sql1, [object_id])
    c.execute(sql1, [object_id])
    conn.commit()


def update_times_played(object_id):
    '''Increments the number of times played for a particular object_id.'''
    current = list(c.execute("select times_played from objects where id =?",[object_id]))[0][0]
    if current == None: current = 0
    c.execute("update objects set times_played =?  where id =?", [current+1,object_id])
    conn.commit()

def num_objects():
    '''Returns the number of objects in database.'''
    return list(c.execute('select COUNT(*) from objects;'))[0][0]


def record_playlog(object_id, asked_questions, right):
    '''Records the questions and responses, and outcomes of each game. Allows us
       to experiment using different parameters without having to retrain from scratch.'''
    r=0
    if right:
        r=1
    sql = "INSERT INTO playlog (object_id,data,right) VALUES (?,?,?)"
    c.execute(sql,[object_id,asked_questions,r])

def flush_tables():
    '''Deletes everything from the database. BEWARE!'''
    c.execute('DELETE FROM objects')
    c.execute('DELETE FROM data')
    c.execute('DELETE FROM questions')

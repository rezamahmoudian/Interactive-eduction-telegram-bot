from .main_db import *


def login(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()
    query = "UPDATE `students` SET login = 1 WHERE student_number = %d" % int(student_num)
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()


def logout_db(user_id):
    cnx = database_connector()
    cursor = cnx.cursor()
    query = "UPDATE `students` SET login = 0 WHERE id = %d" % user_id
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()


def check_log(user_id):
    cnx = database_connector()
    cursor = cnx.cursor()
    check = False
    query = "SELECT login FROM students WHERE id = %d" % user_id
    cursor.execute(query)
    for data in cursor:
        if data[0] == 1:
            check = True
        else:
            check = False
    cursor.close()
    cnx.close()
    return check


def check_student_number(student_number):
    cnx = database_connector()
    cursor = cnx.cursor()
    check = False
    query = "SELECT student_number FROM students"
    cursor.execute(query)
    for data in cursor:
        for student_num in data:
            if student_num == student_number:
                check = True
    cursor.close()
    cnx.close()
    return check


def check_student_data(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()
    check = False
    query = ("SELECT id FROM students WHERE student_number = %d" % student_num)
    cursor.execute(query)
    for data in cursor:
        for id in data:
            if id != -1:
                check = True
    cursor.close()
    cnx.close()
    return check


def check_password_from_db(student_num, password):
    cnx = database_connector()
    cursor = cnx.cursor()
    check = False
    query = ("SELECT password FROM students WHERE student_number = {}".format(student_num))
    cursor.execute(query)
    for data in cursor:
        for p in data:
            if p == password:
                check = True
    cursor.close()
    cnx.close()
    return check


def check_telegram_id_exist(user_id):
    cnx = database_connector()
    cursor = cnx.cursor()
    check = False
    query = "SELECT id FROM students"
    cursor.execute(query)
    for data in cursor:
        for id in data:
            if id == user_id:
                check = True
    cursor.close()
    cnx.close()
    return check


def add_student(user_id, user_data):
    items = []
    sex = ''
    for key, value in user_data.items():
        items.append(value)
    if items[3] == 'مرد':
        sex = 'M'
    elif items[3] == 'زن':
        sex = 'F'
    # add user to the database
    cnx = database_connector()
    cursor = cnx.cursor()

    update_student = ("UPDATE students"
                      " SET id = %s, first_name = %s, last_name = %s, sex = %s, password = %s"
                      "WHERE student_number = %s")
    data_student = (user_id, items[1], items[2], sex, items[4], items[0])
    cursor.execute(update_student, data_student)
    cnx.commit()
    cursor.close()
    cnx.close()

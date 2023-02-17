import mysql.connector
from mysql.connector import errorcode
import random
import os
from dotenv import load_dotenv


def database_connector():
    cnx = mysql.connector.connect(host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), user=os.getenv('DATABASE_USER'),
                                  password=os.getenv('DATABASE_PASS'),
                                  database=os.getenv('DB_NAME'))
    return cnx


def database_disconect(cnx):
    cnx.close()


# USERS
def create_database():
    DB_NAME = os.getenv('DB_NAME')
    TABLES = {}
    TABLES['students'] = (
        "CREATE TABLE `students` ("
        "  `id` int(11) NOT NULL,"
        "  `student_number` int(8) NOT NULL,"
        "  `first_name` varchar(14) NOT NULL,"
        "  `last_name` varchar(16) NOT NULL,"
        "  `password` varchar(20) NOT NULL,"
        "  `sex` enum('M','F') NOT NULL,"
        "  `login` int(2) NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    TABLES['subjects'] = (
        "CREATE TABLE `subjects` ("
        "  `id` int(11) NOT NULL,"
        "  `week` int(8) NOT NULL,"
        "  `title` varchar(200) NOT NULL,"
        "  `description` text ,"
        "  `topic` varchar(20) NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    TABLES['cards'] = (
        "CREATE TABLE `cards` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `student_id` int(8) NOT NULL,"
        "  `subject_id` int(8) NOT NULL,"
        "  PRIMARY KEY (`id`),"
        "   FOREIGN KEY (student_id) REFERENCES students(student_number),"
        "   FOREIGN KEY (subject_id) REFERENCES subjects(id)"
        ") ENGINE=InnoDB")

    TABLES['leader_cards'] = (
        "CREATE TABLE `leader_cards` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `student_id` int(8) NOT NULL,"
        "  `topic` varchar(200) NOT NULL,"
        "  `description` text ,"
        "  PRIMARY KEY (`id`),"
        "   FOREIGN KEY (student_id) REFERENCES students(student_number)"
        ") ENGINE=InnoDB")

    cnx = database_connector()
    cursor = cnx.cursor()

    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    database_disconect(cnx)


def login(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()

    query = "UPDATE `students` SET login = 1 WHERE student_number = %d" % int(student_num)
    cursor.execute(query)
    cnx.commit()

    cursor.close()
    database_disconect(cnx)


def logout_db(user_id):
    cnx = database_connector()
    cursor = cnx.cursor()

    query = "UPDATE `students` SET login = 0 WHERE id = %d" % user_id

    cursor.execute(query)
    cnx.commit()
    cursor.close()
    database_disconect(cnx)


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
    database_disconect(cnx)
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
    database_disconect(cnx)
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
    database_disconect(cnx)
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
    database_disconect(cnx)
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
    database_disconect(cnx)
    return check


def add_student(user_id, user_data):
    items = []
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
    # add_student = ("INSERT INTO students "
    #                "(id, student_number, first_name, last_name, sex)"
    #                "VALUES (%s, %s, %s, %s, %s)")

    data_student = (user_id, items[1], items[2], sex, items[4], items[0])
    cursor.execute(update_student, data_student)
    cnx.commit()

    cursor.close()
    database_disconect(cnx)


# ADMINS

def get_man_students():
    man = []
    cnx = database_connector()
    cursor = cnx.cursor()

    queryM = "SELECT * FROM students WHERE sex = 'M' and login = 1"
    cursor.execute(queryM)
    for data in cursor:
        man.append(data[1])
    cursor.close()
    database_disconect(cnx)
    return man


def get_female_students():
    female = []
    cnx = database_connector()
    cursor = cnx.cursor()

    queryF = "SELECT * FROM students WHERE sex = 'F' and login = 1"

    cursor.execute(queryF)
    for data in cursor:
        female.append(data[1])

    cursor.close()
    database_disconect(cnx)
    return female


def create_leader_cards(man, female):
    cnx = database_connector()
    cursor = cnx.cursor()

    topics = []
    query_cards = "SELECT * FROM subjects;"
    cursor.execute(query_cards)
    for data in cursor:
        topics.append(data[4])

    topics = list(dict.fromkeys(topics))
    cursor.close()
    database_disconect(cnx)
    leader_cards = []
    if len(man) > len(female):
        for i in range(len(topics)):
            card = []
            card.append(topics[i])
            card.append(man[0])
            man.pop(0)
            leader_cards.append(card)
    return leader_cards


def create_cards():
    cnx = database_connector()
    cursor = cnx.cursor()

    man = get_man_students()
    female = get_female_students()

    random.shuffle(man)
    random.shuffle(female)

    leader_cards = create_leader_cards(man, female)
    add_leader_cards_db(leader_cards)

    subjects = []
    query_cards = "SELECT * FROM subjects;"
    cursor.execute(query_cards)
    for data in cursor:
        subjects.append(data[0])

    cursor.close()
    database_disconect(cnx)

    cards = []

    len_subjects = len(subjects)
    while len(man) != 0 and len(female) != 0:
        if len(subjects) != 0:
            for i in range(len_subjects):
                card = []
                card.append(subjects[0])
                subjects.pop(0)
                card.append(man[0])
                man.pop(0)
                card.append(female[0])
                female.pop(0)
                cards.append(card)
        else:
            break

    if len(subjects) != 0:
        for i in range(len_subjects):
            card = []
            card.append(subjects[0])
            subjects.pop(0)
            card.append(man[0])
            man.pop(0)
            cards.append(card)

    print(cards)
    print(man)
    print(female)

    people = man + female
    print(people)

    while len(people) != 0:
        for i in range(len(cards)):
            if len(people) != 0:
                cards[i].append(people[0])
                people.pop(0)
            else:
                break

    print(people)
    print(cards)
    return cards


def add_leader_cards_db(leader_cards):
    cnx = database_connector()
    cursor = cnx.cursor()
    for data in leader_cards:
        add_card = "INSERT INTO leader_cards (`student_id`,`topic`,`description`) VALUES" \
                   " ( {student_id} , '{topic}' , 'description');".format(student_id=data[1], topic=str(data[0]))
        cursor.execute(add_card)
        cursor = cnx.cursor()

    cnx.commit()

    cursor.close()
    database_disconect(cnx)


def get_leader_nums():
    cnx = database_connector()
    cursor = cnx.cursor()
    # get_leader_topic(9901123)
    # get_leader_description(9901119)
    query = "SELECT student_id FROM leader_cards;"
    cursor.execute(query)
    leader_nums = []
    for data in cursor:
        for student_num in data:
            leader_nums.append(student_num)
    print(leader_nums)
    cursor.close()
    database_disconect(cnx)
    return leader_nums


def get_student_chat_id(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()
    student_chat_id = 1
    query = "SELECT id FROM students WHERE student_number=%d;" % student_num
    cursor.execute(query)
    for data in cursor:
        student_chat_id = data[0]
    cursor.close()
    database_disconect(cnx)
    return student_chat_id


def get_student_fname(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()
    first_name = ''
    query = "SELECT first_name FROM students WHERE student_number=%d;" % student_num
    cursor.execute(query)
    for data in cursor:
        first_name = data[0]
    cursor.close()
    database_disconect(cnx)
    return first_name


def get_student_number(chat_id):
    cnx = database_connector()
    cursor = cnx.cursor()
    student_num = -1
    query = "SELECT student_number FROM students WHERE id=%d;" % chat_id
    cursor.execute(query)
    for data in cursor:
        student_num = data[0]
    print("student num =" + str(student_num))
    cursor.close()
    database_disconect(cnx)
    return int(student_num)


def get_student_lname(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()
    last_name = ''
    query = "SELECT last_name FROM students WHERE student_number=%d;" % student_num
    cursor.execute(query)
    for data in cursor:
        last_name = data[0]
    cursor.close()
    database_disconect(cnx)
    return last_name


def get_leader_topic(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()
    topic = ''
    query = "SELECT topic FROM leader_cards WHERE student_id=%d;" % student_num
    cursor.execute(query)
    for data in cursor:
        topic = data[0]
    cursor.close()
    database_disconect(cnx)
    return topic


def get_leader_description(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()
    description = ''
    query = "SELECT description FROM leader_cards WHERE student_id=%d;" % student_num
    cursor.execute(query)
    for data in cursor:
        description = data[0]
    cursor.close()
    database_disconect(cnx)
    return description


def get_student_nums():
    cnx = database_connector()
    cursor = cnx.cursor()
    query = "SELECT student_id FROM cards;"
    cursor.execute(query)
    student_nums = []
    for data in cursor:
        for student_num in data:
            student_nums.append(student_num)
    cursor.close()
    database_disconect(cnx)
    return student_nums


def get_subject_id(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()
    subject_id = 1
    query = "SELECT subject_id FROM cards WHERE student_id=%d;" % student_num
    cursor.execute(query)
    for data in cursor:
        subject_id = data[0]
    cursor.close()
    database_disconect(cnx)
    return subject_id


def get_subject_title(subject_id):
    cnx = database_connector()
    cursor = cnx.cursor()

    subject_title = ''
    query = "SELECT title FROM subjects WHERE id=%d;" % subject_id
    cursor.execute(query)
    for data in cursor:
        subject_title = data[0]
    cursor.close()
    database_disconect(cnx)
    return subject_title


def get_subject_description(subject_id):
    cnx = database_connector()
    cursor = cnx.cursor()

    subject_description = ''
    query = "SELECT description FROM subjects WHERE id=%d;" % subject_id
    cursor.execute(query)
    for data in cursor:
        subject_description = data[0]
    cursor.close()
    database_disconect(cnx)
    return subject_description


def get_subject_topic(subject_id):
    cnx = database_connector()
    cursor = cnx.cursor()

    subject_topic = ''
    query = "SELECT topic FROM subjects WHERE id=%d;" % subject_id
    cursor.execute(query)
    for data in cursor:
        subject_topic = data[0]
    cursor.close()
    database_disconect(cnx)
    return subject_topic


def add_student_with_admin(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()
    query = "INSERT INTO `students`(`id`,`student_number`,`first_name`,`last_name`,`password`,`sex`,`login`)" \
            "VALUES(-1, %d, '-1','-1','-1','M',-1);" % student_num
    cursor.execute(query)
    cursor.close()
    cnx.commit()
    database_disconect(cnx)


def delete_student_with_admin(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()
    query = "DELETE FROM `students`WHERE student_number=%d;" % student_num
    print(query)
    cursor.execute(query)
    cursor.close()
    cnx.commit()
    database_disconect(cnx)


def get_student_info(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()
    query = "SELECT * FROM students WHERE student_number=%d;;" % student_num
    print(query)
    cursor.execute(query)
    student_info = []
    for data in cursor:
        student_info = data
    print(student_info)
    cursor.close()
    cnx.commit()
    database_disconect(cnx)
    return student_info


def add_subject(user_data):
    items = []
    for key, value in user_data.items():
        if key in ('عنوان موضوع', 'سرفصل موضوع', 'توضیحات موضوع', 'شماره ی هفته'):
            items.append(value)

    print(items)
    # add user to the database
    cnx = database_connector()
    cursor = cnx.cursor()

    update_student = ("INSERT INTO `subjects`(`week`,`title`,`description`,`topic`)VALUES(%d, %s, %s, %s);")
    # add_student = ("INSERT INTO students "
    #                "(id, student_number, first_name, last_name, sex)"
    #                "VALUES (%s, %s, %s, %s, %s)")

    data_sub = (items[3], items[0], items[2], items[1])
    print(update_student)
    print(data_sub)
    cursor.execute(update_student, data_sub)
    cnx.commit()

    cursor.close()
    database_disconect(cnx)

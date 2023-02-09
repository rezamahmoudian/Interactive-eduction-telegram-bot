import mysql.connector
from mysql.connector import errorcode


def create_database():
    DB_NAME = 'telegram_bot'
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

    TABLES['cards'] = (
        "CREATE TABLE `cards` ("
        "  `id` int(11) NOT NULL,"
        "  `week` int(8) NOT NULL,"
        "  `title` varchar(200) NOT NULL,"
        "  `description` text ,"
        "  `topic` varchar(20) NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    TABLES['cards1'] = (
        "CREATE TABLE `cards1` ("
        "  `id` int(11) NOT NULL,"
        "  `student_id` int(8) NOT NULL,"
        "  `subject_id` int(8) NOT NULL,"
        "  PRIMARY KEY (`id`),"
        "   FOREIGN KEY (student_id) REFERENCES students(student_number),"
        "   FOREIGN KEY (subject_id) REFERENCES cards(id)"
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

    cnx = mysql.connector.connect(user='root', password='1234', host='127.0.0.1')
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
    cnx.close()


def login(student_num):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    query = "UPDATE `telegram_bot`.`students` SET login = 1 WHERE student_number = %d" % int(student_num)
    print(query)
    cursor.execute(query)
    cnx.commit()

    cursor.close()
    cnx.close()


def logout_db(user_id):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    query = "UPDATE `telegram_bot`.`students` SET login = 0 WHERE id = %d" % user_id
    print(query)

    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()


def check_log(user_id):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
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
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    check = False
    query = "SELECT student_number FROM students"
    cursor.execute(query)
    for data in cursor:
        for student_num in data:
            print(student_num)
            if student_num == student_number:
                check = True

    cursor.close()
    cnx.close()
    return check


def check_student_data(student_num):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    check = False
    query = ("SELECT id FROM students WHERE student_number = %d" % student_num)
    cursor.execute(query)
    for data in cursor:
        for id in data:
            print(id)
            if id != -1:
                check = True

    cursor.close()
    cnx.close()
    return check


def check_password_from_db(student_num, password):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    check = False
    query = ("SELECT password FROM students WHERE student_number = {}".format(student_num))
    print(query)
    cursor.execute(query)
    for data in cursor:
        for p in data:
            print(id)
            if p == password:
                check = True

    cursor.close()
    cnx.close()
    return check


def check_telegram_id_exist(user_id):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    check = False
    query = "SELECT id FROM students"
    cursor.execute(query)
    for data in cursor:
        for id in data:
            print(id)
            if id == user_id:
                check = True

    cursor.close()
    cnx.close()
    return check


def add_student(user_id, user_data):
    items = []
    for key, value in user_data.items():
        items.append(value)
    print(items)
    if items[3] == 'مرد':
        sex = 'M'
    elif items[3] == 'زن':
        sex = 'F'

    # add user to the database
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    update_student = ("UPDATE students"
                      " SET id = %s, first_name = %s, last_name = %s, sex = %s, password = %s"
                      "WHERE student_number = %s")
    print(update_student)
    # add_student = ("INSERT INTO students "
    #                "(id, student_number, first_name, last_name, sex)"
    #                "VALUES (%s, %s, %s, %s, %s)")

    data_student = (user_id, items[1], items[2], sex, items[4], items[0])
    print("262_ ", data_student)
    cursor.execute(update_student, data_student)
    cnx.commit()

    cursor.close()
    cnx.close()

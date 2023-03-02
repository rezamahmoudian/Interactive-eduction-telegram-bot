import mysql.connector
from mysql.connector import errorcode
import random
import os


def database_connector():
    cnx = mysql.connector.connect(host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), user=os.getenv('DATABASE_USER'),
                                  password=os.getenv('DATABASE_PASS'),
                                  database=os.getenv('DB_NAME'))
    return cnx


def create_database():
    DB_NAME = os.getenv('DB_NAME')
    TABLES = {}
    TABLES['students'] = (
        "CREATE TABLE `students` ("
        "  `id` int(11) NOT NULL,"
        "  `student_number` int NOT NULL,"
        "  `first_name` varchar(50) NOT NULL,"
        "  `last_name` varchar(50) NOT NULL,"
        "  `password` varchar(100) NOT NULL,"
        "  `sex` enum('M','F') NOT NULL,"
        "  `login` int(2) NOT NULL,"
        "  PRIMARY KEY (`student_number`)"
        ") ENGINE=InnoDB")

    TABLES['subjects'] = (
        "CREATE TABLE `subjects` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
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
    cnx.close()

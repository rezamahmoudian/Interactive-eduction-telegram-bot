import mysql.connector
from mysql.connector import errorcode


def login(student_num):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    query = "UPDATE `telegram_bot`.`students` SET login = 1 WHERE student_number = %d" % int(student_num)
    print(query)
    cursor.execute(query)
    cnx.commit()

    cursor.close()
    cnx.close()
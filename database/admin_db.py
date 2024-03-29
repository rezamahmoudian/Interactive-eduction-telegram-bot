from .main_db import *


def get_man_students():
    man = []
    cnx = database_connector()
    cursor = cnx.cursor()
    queryM = "SELECT * FROM students WHERE sex = 'M' and login = 1"
    cursor.execute(queryM)
    for data in cursor:
        man.append(data[1])
    cursor.close()
    cnx.close()
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
    cnx.close()
    return female


def create_leader_cards(man, female, week):
    cnx = database_connector()
    cursor = cnx.cursor()
    topics = []
    query_cards = ("SELECT * FROM subjects WHERE week=%d;" % week)
    cursor.execute(query_cards)
    for data in cursor:
        topics.append(data[4])
    topics = list(dict.fromkeys(topics))
    cursor.close()
    leader_cards = []
    if len(man) > len(female):
        for i in range(len(topics)):
            card = []
            card.append(topics[i])
            card.append(man[0])
            man.pop(0)
            leader_cards.append(card)
    cnx.close()
    print("leader_cards: "+str(leader_cards))
    return leader_cards


def create_cards(week):
    cnx = database_connector()
    cursor = cnx.cursor()
    man = get_man_students()
    female = get_female_students()
    random.shuffle(man)
    random.shuffle(female)
    # leader_cards = create_leader_cards(man, female, week)
    # add_leader_cards_db(leader_cards)
    subjects = []
    query_cards = ("SELECT * FROM subjects WHERE week=%d;" % week)
    cursor.execute(query_cards)
    for data in cursor:
        subjects.append(data[0])
    cursor.close()
    cnx.close()
    cards = []
    print("man:" + str(man))
    print("female:" + str(female))
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
                if len(man) == 0 or len(female) == 0:
                    break
            if len(man) == 0 or len(female) == 0:
                break
        else:
            break
    len_subjects = len(subjects)
    if len(subjects) != 0 and len(man) > len(female):
        for i in range(len_subjects):
            card = []
            card.append(subjects[0])
            subjects.pop(0)
            card.append(man[0])
            man.pop(0)
            if len(man) == 0:
                cards.append(card)
                break
            card.append(man[0])
            man.pop(0)
            if len(man) == 0:
                cards.append(card)
                break
            cards.append(card)
    print("cards:" + str(cards))
    people = man + female
    print("people:" + str(people))
    while len(people) != 0:
        for i in range(len(cards)):
            cards[i].append(people[0])
            people.pop(0)
            if len(people) == 0:
                break
    print(people)
    print(cards)
    return cards


def add_leader_cards_db(leader_cards):
    cnx = database_connector()
    cursor = cnx.cursor()
    for data in leader_cards:
        description = f"درباره ی موضوع {data[0]} اطلاعات کسب کنید و گروه خود را برای ارائه ی این موضوع مدیریت کنید."
        add_card = "INSERT INTO leader_cards (`student_id`,`topic`,`description`) VALUES" \
                   " ( {student_id} , '{topic}' , '{des}');".format(student_id=data[1], topic=str(data[0]),
                                                                    des=description)
        cursor.execute(add_card)
        cursor = cnx.cursor()
    cnx.commit()
    cursor.close()
    cnx.close()


def get_leader_nums():
    cnx = database_connector()
    cursor = cnx.cursor()
    query = "SELECT student_id FROM leader_cards;"
    cursor.execute(query)
    leader_nums = []
    for data in cursor:
        for student_num in data:
            leader_nums.append(student_num)
    print(leader_nums)
    cursor.close()
    cnx.close()
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
    cnx.close()
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
    cnx.close()
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
    cnx.close()
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
    cnx.close()
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
    cnx.close()
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
    cnx.close()
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
    cnx.close()
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
    cnx.close()
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
    cnx.close()
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
    cnx.close()
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
    cnx.close()
    return subject_topic


def add_student_with_admin(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()
    query = "INSERT INTO `students`(`id`,`student_number`,`first_name`,`last_name`,`password`,`sex`,`login`)" \
            "VALUES(-1, %d, '-1','-1','-1','M',-1);" % student_num
    cursor.execute(query)
    cursor.close()
    cnx.commit()
    cnx.close()


def delete_student_with_admin(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()
    query = "DELETE FROM `students`WHERE student_number=%d;" % student_num
    print(query)
    cursor.execute(query)
    cursor.close()
    cnx.commit()
    cnx.close()


def get_student_info(student_num):
    cnx = database_connector()
    cursor = cnx.cursor()
    query = "SELECT * FROM students WHERE student_number=%d;" % student_num
    print(query)
    cursor.execute(query)
    student_info = []
    for data in cursor:
        student_info = data
    print(student_info)
    cursor.close()
    cnx.commit()
    cnx.close()
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

    print("week =" + str(items[3]))
    print("title =" + str(items[0]))
    print("descrip =" + str(items[2]))
    print("topic =" + str(items[1]))

    update_student = "INSERT INTO `subjects`(`week`,`title`,`description`,`topic`)VALUES" \
                     "('{week}', '{title}', '{des}', '{topic}'); ".format(week=int(items[3]), title=items[0],
                                                                          des=items[2], topic=items[1])
    print(update_student)
    cursor.execute(update_student)
    cnx.commit()
    cursor.close()
    cnx.close()


def db_del_sub(id):
    cnx = database_connector()
    cursor = cnx.cursor()
    query = "DELETE FROM `subjects` WHERE (`id` = %d);" % int(id)
    cursor.execute(query)
    cursor.close()
    cnx.commit()
    cnx.close()


def db_get_subjects():
    cnx = database_connector()
    cursor = cnx.cursor()
    subjects = []
    query = "SELECT * FROM subjects;"
    cursor.execute(query)
    for data in cursor:
        subjects.append(str(data))
    cursor.close()
    cnx.close()
    return subjects


def db_get_students():
    cnx = database_connector()
    cursor = cnx.cursor()
    students = []
    query = "SELECT * FROM students;"
    cursor.execute(query)
    for data in cursor:
        students.append(str(data))
    cursor.close()
    cnx.close()
    return students

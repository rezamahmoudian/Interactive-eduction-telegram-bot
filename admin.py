import mysql.connector
from mysql.connector import errorcode
import random
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from main import bot

admin_reply_keyboard = [['حذف موضوع', 'افزودن موضوع'],
                        ['حذف همه ی موضوعات', 'نمایش موضوعات'],
                        ['بازگردانی کارتها', 'پخش کارتها', 'ایجاد کارتها'],
                        ['مشاهده ی اطلاعات کاربران']]
admin_markup = ReplyKeyboardMarkup(admin_reply_keyboard, resize_keyboard=True, one_time_keyboard=True)

CHECKADMINPASS, CHOOSEACTION, ADDSUB, DELETESUB, SHOWSUBJECTS, DELETEALLSUBJECTS, CREATECARDS, BROADCASTCARDS, RETURNCARDS, SHOWUSERINFORMATION = range(
    10)


async def admin(update, context):
    user = update.message.from_user
    user_data = context.user_data
    text = update.message.text
    print(text)

    await update.message.reply_text("رمز ورود به عنوان ادمین را وارد کنید:")
    return CHECKADMINPASS


admin_pass = "1234"


async def check_admin_pass(update, context):
    user = update.message.from_user
    user_data = context.user_data

    text = update.message.text
    check = text == admin_pass
    if check:
        await update.message.reply_text("با موفقیت وارد شدید.", reply_markup=admin_markup)
        return CHOOSEACTION
    else:
        await update.message.reply_text("رمز ورود صحیح نیست. لطفا دوباره سعی کنید.")

        return CHECKADMINPASS


async def choose_action(update, context):
    user = update.message.from_user
    user_data = context.user_data

    text = update.message.text
    if text == 'افزودن موضوع':
        return ADDSUB
    elif text == 'حذف موضوع':
        return DELETESUB
    elif text == 'نمایش موضوعات':
        return SHOWSUBJECTS
    elif text == 'حذف همه ی موضوعات':
        return DELETEALLSUBJECTS
    elif text == 'ایجاد کارتها':
        return CREATECARDS
    elif text == 'پخش کارتها':
        return BROADCASTCARDS
    elif text == 'بازگردانی کارتهای پخش شده':
        return RETURNCARDS
    elif text == 'مشاهده ی اطلاعات کاربران':
        return SHOWUSERINFORMATION
    else:
        await update.message.reply_text("لطفا دستور صحیح را وارد کنید.")
        return CHOOSEACTION


def get_man_students():
    man = []
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    queryM = "SELECT * FROM telegram_bot.students WHERE sex = 'M' and login = 1"
    cursor.execute(queryM)
    for data in cursor:
        man.append(data[1])
    cursor.close()
    cnx.close()
    return man


def get_female_students():
    female = []
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    queryF = "SELECT * FROM telegram_bot.students WHERE sex = 'F' and login = 1"

    cursor.execute(queryF)
    for data in cursor:
        female.append(data[1])

    cursor.close()
    cnx.close()
    return female


def create_leader_cards(man, female):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    topics = []
    query_cards = "SELECT * FROM telegram_bot.cards;"
    cursor.execute(query_cards)
    for data in cursor:
        print(data)
        topics.append(data[4])

    topics = list(dict.fromkeys(topics))
    print(topics)
    cursor.close()
    cnx.close()
    leader_cards = []
    if len(man) > len(female):
        for i in range(len(topics)):
            card = []
            card.append(topics[i])
            card.append(man[0])
            man.pop(0)
            leader_cards.append(card)
    print("cards: ")
    print(leader_cards)
    print(man)
    return leader_cards


def create_cards():
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    man = get_man_students()
    female = get_female_students()

    random.shuffle(man)
    random.shuffle(female)
    print(man)
    print(female)

    leader_cards = create_leader_cards(man, female)
    add_leader_cards_db(leader_cards)

    subjects = []
    query_cards = "SELECT * FROM telegram_bot.cards;"
    cursor.execute(query_cards)
    for data in cursor:
        print(data)
        subjects.append(data[0])

    print(subjects)
    cursor.close()
    cnx.close()

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
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()
    for data in leader_cards:
        add_card = "INSERT INTO `telegram_bot`.`leader_cards`(`student_id`,`topic`,`description`) VALUES" \
                   " ( {student_id} , '{topic}' , 'description');".format(student_id=data[1], topic=str(data[0]))
        print(add_card)
        cursor.execute(add_card)
        cursor = cnx.cursor()

    cnx.commit()

    cursor.close()
    cnx.close()


async def add_cards_db(update, context):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()
    delete_leader_cards = "DELETE FROM leader_cards WHERE id != 0;"
    cursor.execute(delete_leader_cards)

    cursor = cnx.cursor()
    delete_cards = "DELETE FROM cards1 WHERE id != 0;"
    cursor.execute(delete_cards)
    cnx.commit()
    cursor.close()
    cards = create_cards()
    cursor = cnx.cursor()
    for data in cards:
        for i in range(len(data) - 1):
            add_card = "INSERT INTO `telegram_bot`.`cards1`(`student_id`,`subject_id`) VALUES " \
                       "({student_id},{subject_id})".format(student_id=data[i + 1], subject_id=data[0])
            print(add_card)
            cursor.execute(add_card)
            cursor = cnx.cursor()
    cnx.commit()
    cursor.close()
    cnx.close()
    await update.message.reply_text("کارتها با موفقیت در دیتابیس ایجاد شدند.")
    return CHOOSEACTION


def get_leader_nums():
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()
    # get_leader_topic(9901123)
    # get_leader_description(9901119)
    query = "SELECT student_id FROM telegram_bot.leader_cards;"
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
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()
    student_chat_id = 1
    query = "SELECT id FROM telegram_bot.students WHERE student_number=%d;" % student_num
    cursor.execute(query)
    for data in cursor:
        student_chat_id = data[0]
    cursor.close()
    cnx.close()
    print(student_chat_id)
    return student_chat_id


def get_student_fname(student_num):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()
    first_name = ''
    query = "SELECT first_name FROM telegram_bot.students WHERE student_number=%d;" % student_num
    cursor.execute(query)
    for data in cursor:
        first_name = data[0]
    cursor.close()
    cnx.close()
    print(first_name)
    return first_name


def get_student_lname(student_num):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()
    last_name = ''
    query = "SELECT last_name FROM telegram_bot.students WHERE student_number=%d;" % student_num
    cursor.execute(query)
    for data in cursor:
        last_name = data[0]
    cursor.close()
    cnx.close()
    print(last_name)
    return last_name


def get_leader_topic(student_num):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()
    topic = ''
    query = "SELECT topic FROM telegram_bot.leader_cards WHERE student_id=%d;" % student_num
    cursor.execute(query)
    for data in cursor:
        topic = data[0]
    cursor.close()
    cnx.close()
    print(topic)
    return topic


def get_leader_description(student_num):
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()
    description = ''
    query = "SELECT description FROM telegram_bot.leader_cards WHERE student_id=%d;" % student_num
    cursor.execute(query)
    for data in cursor:
        description = data[0]
    cursor.close()
    cnx.close()
    print(description)
    return description


async def broadcast_leader_cards():
    leader_nums = get_leader_nums()
    for student_number in leader_nums:
        first_name = get_student_fname(student_number)
        last_name = get_student_lname(student_number)
        chat_id = get_student_chat_id(student_number)
        topic = get_leader_topic(student_number)
        description = get_leader_description(student_number)

        text = " \n سلام {fname} {lname} عزیز با شماره دانشجویی {student_num}" \
               "\n شما در جلسه ی آینده به عنوان سرگروه انتخاب شده اید" \
               " \n.میباشد {top} موضوع گروه شما در جلسه ی آینده " \
               "\n{descrip} :توضیحات".format(fname=first_name, lname=last_name, student_num=student_number, top=topic,
                                             descrip=description)
        print(text)
        try:
            await bot.send_message(chat_id=chat_id, text=text)
        except:
            print("chat with id %d not fount" % chat_id)


def broadcast_cards():
    pass


if __name__ == '__main__':
    broadcast_leader_cards()

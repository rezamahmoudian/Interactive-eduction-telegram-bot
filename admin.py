import mysql.connector
from mysql.connector import errorcode
import random


# admin_reply_keyboard = [['حذف موضوع', 'افزودن موضوع'],
#                   ['حذف همه ی موضوعات', 'نمایش موضوعات'],
#                   ['بازگردانی کارتهای پخش شده', 'پخش کارتها'],
#                   ['مشاهده ی اطلاعات کاربران']]
# admin_markup = ReplyKeyboardMarkup(admin_reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
#
# CHECKADMINPASS, CHOOSEACTION, ADDSUB, DELETESUB, SHOWSUBJECTS, DELETEALLSUBJECTS, BROADCASTCARDS, RETURNCARDS, SHOWUSERINFORMATION = range(9)
#
#
# async def admin(update, context):
#     user = update.message.from_user
#     user_data = context.user_data
#     text = update.message.text
#     print(text)
#
#     await update.message.reply_text("رمز ورود به عنوان ادمین را وارد کنید:")
#     return CHECKADMINPASS
#
#
# admin_pass = "1234"
#
#
# async def check_admin_pass(update, context):
#     user = update.message.from_user
#     user_data = context.user_data
#
#     text = update.message.text
#     check = text == admin_pass
#     if check:
#         await update.message.reply_text("با موفقیت وارد شدید.", reply_markup=admin_markup)
#         return CHOOSEACTION
#     else:
#         await update.message.reply_text("رمز ورود صحیح نیست. لطفا دوباره سعی کنید.")
#
#         return CHECKPASSWORD
#
#
# async def choose_action(update, context):
#     user = update.message.from_user
#     user_data = context.user_data
#
#     text = update.message.text
#     if text == 'افزودن موضوع':
#         return ADDSUB
#     elif text == 'حذف موضوع':
#         return DELETESUB
#     elif text == 'نمایش موضوعات':
#         return SHOWSUBJECTS
#     elif text == 'حذف همه ی موضوعات':
#         return DELETEALLSUBJECTS
#     elif text == 'پخش کارتها':
#         return BROADCASTCARDS
#     elif text == 'بازگردانی کارتهای پخش شده':
#         return RETURNCARDS
#     elif text == 'مشاهده ی اطلاعات کاربران':
#         return SHOWUSERINFORMATION
#     else:
#         await update.message.reply_text("لطفا دستور صحیح را وارد کنید.")
#         return CHOOSEACTION
#

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

    create_leader_cards(man, female)

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


if __name__ == '__main__':
    create_cards()

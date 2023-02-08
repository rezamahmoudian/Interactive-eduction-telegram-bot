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


def create_cards():
    man = []
    female = []
    cnx = mysql.connector.connect(user='root', password='1234', database='telegram_bot')
    cursor = cnx.cursor()

    check = False
    queryM = "SELECT * FROM telegram_bot.students WHERE sex = 'M' and login = 1"
    queryF = "SELECT * FROM telegram_bot.students WHERE sex = 'F' and login = 1"
    cursor.execute(queryM)

    for data in cursor:
        man.append(data[1])
    cursor.execute(queryF)
    for data in cursor:
        female.append(data[1])
    random.shuffle(man)
    random.shuffle(female)
    print(man)
    print(female)


    subjects = []
    topics = []
    query_cards = "SELECT * FROM telegram_bot.cards;"
    cursor.execute(query_cards)
    for data in cursor:
        print(data)
        topics.append(data[4])
        subjects.append(data[0])

    topics = list(dict.fromkeys(topics))

    # for key in topics:
    #     topics[key] = []
    # cursor.execute(query_cards)
    # for data in cursor:
    #     for key in topics:
    #         print("key "+ key)
    #         print("data "+ data[4])
    #
    #         if data[4] == key:
    #             topics[key].append(data[2])

    print(topics)
    print(subjects)
    cursor.close()
    cnx.close()

    admin_cards = []
    if len(man)>len(female):
        for i in range(len(topics)):
            card = []
            card.append(topics[i])
            card.append(man[0])
            man.pop(0)
            admin_cards.append(card)

    print("cards: ")
    print(admin_cards)
    print(man)

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
            cards[i].append(people[0])
            people.pop(0)

    print(people)
    print(cards)



if __name__ == '__main__':
    create_cards()


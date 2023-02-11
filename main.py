from __future__ import print_function
import logging
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, filters, ConversationHandler, ApplicationBuilder,InlineQueryHandler)
import os
import mysql.connector
from mysql.connector import errorcode
from database_modules import *
from users import *
from admin import *
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = telegram.Bot(token=TOKEN)

PORT = int(os.environ.get('PORT', 5000))


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('login', start)],

        states={
            STUDENT_NUMBER: [CommandHandler('start', start), CommandHandler('login', start),
                             MessageHandler(filters.TEXT, student_number)],
            FNAME: [CommandHandler('start', start), CommandHandler('login', start),
                    MessageHandler(filters.TEXT, fname)],
            LNAME: [CommandHandler('start', start), CommandHandler('login', start),
                    MessageHandler(filters.TEXT, lname)],
            SEX: [CommandHandler('start', start), CommandHandler('login', start), MessageHandler(filters.TEXT, sex)],
            PASSWORD: [CommandHandler('start', start), CommandHandler('login', start),
                       MessageHandler(filters.TEXT, password)],
            CHECKPASSWORD: [CommandHandler('start', start), CommandHandler('login', start),
                            MessageHandler(filters.TEXT, check_password)],
            CONFIRMATION: [CommandHandler('start', start), CommandHandler('login', start),
                           MessageHandler(filters.Regex('^مورد تایید است$'), confirmation),
                           MessageHandler(filters.Regex('^شروع دوباره$'), start)]
        },

        fallbacks=[CommandHandler('cancle', cancle)]
    )
    admin_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('admin', admin)],
        states={
            CHECKADMINPASS: [CommandHandler('admin', admin),
                             MessageHandler(filters.TEXT, check_admin_pass)],
            # CHOOSEACTION: [CommandHandler('admin', admin),
            #                MessageHandler(filters.Regex('^ایجاد کارتها$'), add_cards_db),
            #                MessageHandler(filters.Regex('^پخش کارتها$'), broadcast_cards),
            #                ]
            CHOOSEACTION: [CommandHandler('admin', admin),
                           MessageHandler(filters.TEXT, choose_action),
                           ],
            CREATECARDS: [CommandHandler('admin', admin),
                          MessageHandler(filters.Regex('^بله$'), add_cards_db),
                          MessageHandler(filters.Regex('^خیر'), create_card_cancel),
                          ],
            BROADCASTCARDS: [CommandHandler('admin', admin),
                             MessageHandler(filters.Regex('^سرگروه ها$'), broadcast_leader_cards),
                             MessageHandler(filters.Regex('^زیرگروه ها'), broadcast_cards),
                             ]
        },
        fallbacks=[CommandHandler('cancle', cancle)]
    )

    app.add_handler(conv_handler)
    app.add_handler(admin_conv_handler)
    app.add_handler(CommandHandler('logout', logout))

    app.run_polling()


if __name__ == '__main__':
    create_database()
    main()

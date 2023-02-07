from __future__ import print_function
import logging
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, filters, ConversationHandler, ApplicationBuilder)
import os
import mysql.connector
from mysql.connector import errorcode
from database_modules import *
from users import *

TOKEN = "5806507050:AAFVm2zmYpAxDwjQtXr_MaROnYM_eZG8gwI"
bot = telegram.Bot(token=TOKEN)

PORT = int(os.environ.get('PORT', 5000))


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    app = ApplicationBuilder().token("5806507050:AAFVm2zmYpAxDwjQtXr_MaROnYM_eZG8gwI").build()

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

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('logout', logout))
    app.run_polling()


if __name__ == '__main__':
    create_database()
    main()

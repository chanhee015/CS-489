import sys
import pandas as pd
import csv
import time
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ConversationHandler, MessageHandler, Updater, Filters

import dilemma
import generate_empty_files

# 1. 사용자가 /teststart로 test시작. (구현완료)
# 2. 이 id를 확인 (구현완료)
# 3. 해당 id가 'info.csv'에 있는지 확인. 없으면 3-1로, 있으면 3-2로. (csv 파일 형식: ['id', 'age', 'gender', 'job']) (구현완료)
# 3-1. 없으면 age, gender, job을 물어본 후 저장. 3-2로 감. (구현완료)
# 3-2. age, gender, job을 확인 후 해당하는 csv 파일로 감. (구현완료)
# 4. 질문하기 및 그 질문에 대한 평균을 보여주기 (성범) -- 답변이 없었던 질문인데 이게 조합되어 만든 질문일 경우에는 그 평균도 함께 보여줄 수 있어야 함.
# 5. 해당 질문과 그에 대한 답변을 csv에 저장. (ex. '20_male_student.csv'에 [딜레마, 점수] 형식으로 저장 -- 저장 방식은 딜레마 어떻게 조합 및 제공하냐에 따라 달라짐)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
AGE, GENDER, JOB, INFOEND = range(4)

def start(update: Update, context: CallbackContext) -> int:
    info_exist = False
    should_erase = False
    should_erase_temp = False
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! I am Ethics Bot. I will take a short test for ehics. Send /cancel to stop test anytime.\n\n')

    info_file = open('info.csv', 'r', encoding='utf-8', newline='')
    reader = csv.reader(info_file, delimiter=',')
    lines = []

    for line in reader:
        if (int(line[0]) == update.effective_chat.id):
            if (len(line) == 4):
                info_exist = True
                break
            else:
                should_erase = True
                should_erase_temp = True
        lines.append(line)
        if (should_erase_temp):
            lines.pop()
            should_erase_temp = False
    info_file.close()

    if (should_erase):
        info_file = open('info.csv', 'w', newline='')
        writer = csv.writer(info_file)
        writer.writerows(lines)
        info_file.close()

    if (info_exist):
        context.bot.send_message(chat_id=update.effective_chat.id, text='We already have your information.\n Send any word to start test!')
        return INFOEND
    else:
        reply_keyboard = [['20s', '30s', '40s', 'Others']]
        update.message.reply_text(
            'We do not have your information.\n'
            'What is your age?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return AGE

def age(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Male', 'Female', 'Others']]
    user = update.message.from_user
    logger.info("AGE of %s: %s", user.first_name, update.message.text)
    info_file = open('info.csv', 'a', encoding='utf-8', newline='')
    csv.writer(info_file).writerow([update.effective_chat.id, update.message.text])
    info_file.close()
    update.message.reply_text(
        'What is your gender?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return GENDER

def gender(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Student', 'Graduate student', 'Employee'],
                      ['Self-owner', 'Specialized', 'Others']]
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    info_file = open('info.csv', 'r')
    reader = csv.reader(info_file)
    lines = []
    for line in reader:
        if (int(line[0]) == update.effective_chat.id):
            line.append(update.message.text)
        lines.append(line)
    info_file.close()
    info_file = open('info.csv', 'w', newline='')
    writer = csv.writer(info_file)
    writer.writerows(lines)
    info_file.close()
    update.message.reply_text(
        'What is your job?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return JOB

def job(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Job of %s: %s", user.first_name, update.message.text)
    info_file = open('info.csv', 'r')
    reader = csv.reader(info_file)
    lines = []
    for line in reader:
        if (int(line[0]) == update.effective_chat.id):
            line.append(update.message.text)
        lines.append(line)
    info_file.close()
    info_file = open('info.csv', 'w', newline='')
    writer = csv.writer(info_file)
    writer.writerows(lines)
    info_file.close()
    update.message.reply_text(
        'Thanks for adding your information!\n Send any word to start test!',
        reply_markup=ReplyKeyboardRemove()
    )
    return INFOEND

def infoend(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    context.bot.send_message(chat_id=update.effective_chat.id, text='Now the test begins!')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! See you next time!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main() -> None:
    updater = Updater('1452014249:AAF8xlpe6r3sAq0c3ZJ--HH6I5qT5ZBftQs', use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGE: [MessageHandler(Filters.regex('^(20s|30sl|40s|Others)$'), age)],
            GENDER: [MessageHandler(Filters.regex('^(Male|Female|Others)$'), gender)],
            JOB: [MessageHandler(Filters.regex('^(Student|Graduate Student|Others)$'), job)],
            INFOEND: [MessageHandler(Filters.text & ~Filters.command, infoend)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
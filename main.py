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
AGE, GENDER, JOB, ASKQ1, ASKQ2, ASKQ3, PREDQ1, PREDQ2, PREDQ3, ENDTEST = range(10)

def start(update: Update, context: CallbackContext):
    info_exist = False
    should_erase = False
    should_erase_temp = False
    context.bot.send_message(chat_id=update.effective_chat.id, text='안녕하세요, 컴윤사봇입니다. 컴퓨터 윤리와 관련된 간단한 테스트를 진행하겠습니다. 종료를 위해선 언제든지 /cancel 을 입력해주세요.\n\n')

    info_file = open('info.csv', 'r', encoding='utf-8', newline='')
    reader = csv.reader(info_file, delimiter=',')
    lines = []

    for line in reader:
        if (int(line[0]) == update.effective_chat.id):
            if (len(line) >= 4):
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
        info_file = open('info.csv', 'w', encoding='utf-8', newline='')
        writer = csv.writer(info_file)
        writer.writerows(lines)
        info_file.close()

    if (info_exist):
        reply_keyboard = [['시작']]
        update.message.reply_text(
            '이미 사용자 정보를 가지고 있습니다.\n테스트를 시작하겠습니다!',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return ASKQ1
    else:
        reply_keyboard = [['20대', '30대', '40대', '기타']]
        update.message.reply_text(
            '사용자 정보가 없습니다.\n'
            '연령대가 어떻게 되시나요?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return AGE

def age(update: Update, context: CallbackContext):
    reply_keyboard = [['남성', '여성', '기타']]
    user = update.message.from_user
    logger.info("AGE of %s: %s", user.first_name, update.message.text)
    info_file = open('info.csv', 'a', encoding='utf-8', newline='')
    csv.writer(info_file).writerow([update.effective_chat.id, update.message.text])
    info_file.close()
    update.message.reply_text(
        '성별이 어떻게 되시나요?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return GENDER

def gender(update: Update, context: CallbackContext):
    reply_keyboard = [['학생', '대학원생', '회사원'],
                      ['자영업자', '전문직', '기타']]
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    info_file = open('info.csv', 'r', encoding='utf-8', newline='')
    reader = csv.reader(info_file)
    lines = []
    for line in reader:
        if (int(line[0]) == update.effective_chat.id):
            line.append(update.message.text)
        lines.append(line)
    info_file.close()
    info_file = open('info.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(info_file)
    writer.writerows(lines)
    info_file.close()
    update.message.reply_text(
        '직업이 어떻게 되시나요?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return JOB

def job(update: Update, context: CallbackContext):
    user = update.message.from_user
    reply_keyboard = [['시작']]
    logger.info("Job of %s: %s", user.first_name, update.message.text)
    info_file = open('info.csv', 'r', encoding='utf-8', newline='')
    reader = csv.reader(info_file)
    lines = []
    for line in reader:
        if (int(line[0]) == update.effective_chat.id):
            line.append(update.message.text)
        lines.append(line)
    info_file.close()
    info_file = open('info.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(info_file)
    writer.writerows(lines)
    info_file.close()
    update.message.reply_text(
        '정보를 입력해주셔서 감사합니다!\n테스트를 시작합니다!',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return ASKQ1

# def infoend(update: Update, context: CallbackContext):
#     user = update.message.from_user
#     context.bot.send_message(chat_id=update.effective_chat.id, text='테스트를 시작합니다!')
#     return ConversationHandler.END

def askQ1(update: Update, context: CallbackContext):
    reply_keyboard = [['1', '2', '3', '4', '5']]
    user = update.message.from_user
    logger.info("Q1 to %s", user.first_name)
    info_file = open('info.csv', 'r', encoding='utf-8', newline='')
    reader = csv.reader(info_file)
    lines = []
    for line in reader:
        if (int(line[0]) == update.effective_chat.id):
            line.append(dilemma.ran_qlist())
            Q = dilemma.q_out(line[-1][0])
        lines.append(line)
    info_file.close()
    info_file = open('info.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(info_file)
    writer.writerows(lines)
    info_file.close()
    update.message.reply_text(Q, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ASKQ2

def askQ2(update: Update, context: CallbackContext):
    ans = []
    user = update.message.from_user
    logger.info("Q2 to %s", user.first_name)
    reply_keyboard = [['1', '2', '3', '4', '5']]
    info_file = open('info.csv', 'r', encoding='utf-8', newline='')
    reader = csv.reader(info_file)
    for line in reader:
        if (int(line[0]) == update.effective_chat.id):
            [age, gender, job] = line[1:4]
            temp_list = list(map(int, line[-1][1:-1].split(', ')))
            preQ = temp_list[0]
            Q = dilemma.q_out(temp_list[1])
            break
    info_file.close()
    data_file_name = 'answers/' + age + '_' + gender + '_' + job + '.csv'
    data_file = open(data_file_name, 'r', encoding='utf-8', newline='')
    reader = csv.reader(data_file)
    for line in reader:
        if ((int(line[0]) == preQ) and (int(line[1]) != update.effective_chat.id)):
            ans.append(int(line[2]))
    data_file.close()
    data_file = open(data_file_name, 'a', encoding='utf-8', newline='')
    csv.writer(data_file).writerow([temp_list[0], update.effective_chat.id, update.message.text])
    data_file.close()
    if (len(ans) != 0):
        avg = round(sum(ans) / len(ans), 2)
        reply_text = '앞선 문제에 대한 ' + age + ' ' + gender + ' ' + job + '의 평균 답변은 ' + str(avg) + '점이었습니다.'
    else:
        reply_text = '아직 앞선 문제에 대한 ' + age + ' ' + gender + ' ' + job + '의 답변이 충분하지 않아 평균 점수를 제공하지 못하고 있습니다. 감사합니다.'
    update.message.reply_text(reply_text)
    update.message.reply_text(Q, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ASKQ3

def askQ3(update: Update, context: CallbackContext):
    ans = []
    user = update.message.from_user
    logger.info("Q3 to %s", user.first_name)
    reply_keyboard = [['1', '2', '3', '4', '5']]
    info_file = open('info.csv', 'r', encoding='utf-8', newline='')
    reader = csv.reader(info_file)
    for line in reader:
        if (int(line[0]) == update.effective_chat.id):
            [age, gender, job] = line[1:4]
            temp_list = list(map(int, line[-1][1:-1].split(', ')))
            preQ = temp_list[1]
            Q = dilemma.q_out(temp_list[2])
            break
    info_file.close()
    data_file_name = 'answers/' + age + '_' + gender + '_' + job + '.csv'
    data_file = open(data_file_name, 'r', encoding='utf-8', newline='')
    reader = csv.reader(data_file)
    for line in reader:
        if ((int(line[0]) == preQ) and (int(line[1]) != update.effective_chat.id)):
            ans.append(int(line[2]))
    data_file.close()
    data_file = open(data_file_name, 'a', encoding='utf-8', newline='')
    csv.writer(data_file).writerow([temp_list[1], update.effective_chat.id, update.message.text])
    data_file.close()
    if (len(ans) != 0):
        avg = round(sum(ans) / len(ans), 2)
        reply_text = '앞선 문제에 대한 ' + age + ' ' + gender + ' ' + job + '의 평균 답변은 ' + str(avg) + '점이었습니다.'
    else:
        reply_text = '아직 앞선 문제에 대한 ' + age + ' ' + gender + ' ' + job + '의 답변이 충분하지 않아 평균 점수를 제공하지 못하고 있습니다. 감사합니다.'
    update.message.reply_text(reply_text)
    update.message.reply_text(Q, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return PREDQ1

def predQ1(update: Update, context: CallbackContext):
    ans = []
    group_ans = []
    diff = []
    stan = []
    user = update.message.from_user
    logger.info("Pred Q1 to %s", user.first_name)
    reply_keyboard = [['다음']]
    info_file = open('info.csv', 'r', encoding='utf-8', newline='')
    reader = csv.reader(info_file)
    for line in reader:
        if (int(line[0]) == update.effective_chat.id):
            [age, gender, job] = line[1:4]
            temp_list = list(map(int, line[-1][1:-1].split(', ')))
            compQ = temp_list[0]
            preQ = temp_list[2]
            Q = dilemma.q_out(temp_list[3])
            break
    info_file.close()
    data_file_name = 'answers/' + age + '_' + gender + '_' + job + '.csv'
    data_file = open(data_file_name, 'r', encoding='utf-8', newline='')
    reader = csv.reader(data_file)
    for line in reader:
        if (int(line[0]) == compQ):
            if (int(line[1]) == update.effective_chat.id):
                diff.append(int(line[2]))
                continue
            else:
                stan.append(int(line[2]))
                continue
        if ((int(line[0]) == preQ) and (int(line[1]) != update.effective_chat.id)):
            ans.append(int(line[2]))
            continue
        if ((int(line[0]) == temp_list[3]) and (int(line[1]) != update.effective_chat.id)):
            group_ans.append(int(line[2]))
            continue
    data_file.close()
    data_file = open(data_file_name, 'a', encoding='utf-8', newline='')
    csv.writer(data_file).writerow([temp_list[2], update.effective_chat.id, update.message.text])
    data_file.close()
    if (len(ans) != 0):
        avg = round(sum(ans) / len(ans), 2)
        reply_text = '앞선 문제에 대한 ' + age + ' ' + gender + ' ' + job + '의 평균 답변은 ' + str(avg) + '점이었습니다.'
    else:
        reply_text = '아직 앞선 문제에 대한 ' + age + ' ' + gender + ' ' + job + '의 답변이 충분하지 않아 평균 점수를 제공하지 못하고 있습니다. 감사합니다.'
    if ((len(group_ans) == 0) or (len(stan) == 0)):
        Q += '\n\n아직 ' + age + ' ' + gender + ' ' + job + '의 답변이 충분하지 않아 점수 예측을 제공하지 못하고 있습니다. 감사합니다.'
    else:
        difference = (sum(stan) / len(stan)) - (sum(diff) / len(diff))
        group_avg = sum(group_ans) / len(group_ans)
        pred = group_avg - difference
        if (pred < 1):
            pred = 1.00
        elif (pred > 5):
            pred = 5.00
        else:
            pred = round(pred, 2)
        Q += '\n\n이 문제에 대한 당신의 예상 답변은 ' + str(pred) + '점입니다.'
    update.message.reply_text(reply_text)
    update.message.reply_text(Q, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return PREDQ2

def predQ2(update: Update, context: CallbackContext):
    group_ans = []
    diff = []
    stan = []
    user = update.message.from_user
    logger.info("Pred Q2 to %s", user.first_name)
    reply_keyboard = [['다음']]
    info_file = open('info.csv', 'r', encoding='utf-8', newline='')
    reader = csv.reader(info_file)
    for line in reader:
        if (int(line[0]) == update.effective_chat.id):
            [age, gender, job] = line[1:4]
            temp_list = list(map(int, line[-1][1:-1].split(', ')))
            compQ = temp_list[1]
            Q = dilemma.q_out(temp_list[4])
            break
    info_file.close()
    data_file_name = 'answers/' + age + '_' + gender + '_' + job + '.csv'
    data_file = open(data_file_name, 'r', encoding='utf-8', newline='')
    reader = csv.reader(data_file)
    for line in reader:
        if (int(line[0]) == compQ):
            if (int(line[1]) == update.effective_chat.id):
                diff.append(int(line[2]))
                continue
            else:
                stan.append(int(line[2]))
                continue
        if ((int(line[0]) == temp_list[4]) and (int(line[1]) != update.effective_chat.id)):
            group_ans.append(int(line[2]))
            continue
    data_file.close()
    if ((len(group_ans) == 0) or (len(stan) == 0)):
        Q += '\n\n아직 ' + age + ' ' + gender + ' ' + job + '의 답변이 충분하지 않아 점수 예측을 제공하지 못하고 있습니다. 감사합니다.'
    else:
        difference = (sum(stan) / len(stan)) - (sum(diff) / len(diff))
        group_avg = sum(group_ans) / len(group_ans)
        pred = group_avg - difference
        if (pred < 1):
            pred = 1.00
        elif (pred > 5):
            pred = 5.00
        else:
            pred = round(pred, 2)
        Q += '\n\n이 문제에 대한 당신의 예상 답변은 ' + str(pred) + '점입니다.'
    update.message.reply_text(Q, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return PREDQ3

def predQ3(update: Update, context: CallbackContext):
    group_ans = []
    diff = []
    stan = []
    user = update.message.from_user
    logger.info("Pred Q3 to %s", user.first_name)
    reply_keyboard = [['다음']]
    info_file = open('info.csv', 'r', encoding='utf-8', newline='')
    reader = csv.reader(info_file)
    for line in reader:
        if (int(line[0]) == update.effective_chat.id):
            [age, gender, job] = line[1:4]
            temp_list = list(map(int, line[-1][1:-1].split(', ')))
            compQ = temp_list[2]
            Q = dilemma.q_out(temp_list[5])
            break
    info_file.close()
    data_file_name = 'answers/' + age + '_' + gender + '_' + job + '.csv'
    data_file = open(data_file_name, 'r', encoding='utf-8', newline='')
    reader = csv.reader(data_file)
    for line in reader:
        if (int(line[0]) == compQ):
            if (int(line[1]) == update.effective_chat.id):
                diff.append(int(line[2]))
                continue
            else:
                stan.append(int(line[2]))
                continue
        if ((int(line[0]) == temp_list[5]) and (int(line[1]) != update.effective_chat.id)):
            group_ans.append(int(line[2]))
            continue
    data_file.close()
    if ((len(group_ans) == 0) or (len(stan) == 0)):
        Q += '\n\n아직 ' + age + ' ' + gender + ' ' + job + '의 답변이 충분하지 않아 점수 예측을 제공하지 못하고 있습니다. 감사합니다.'
    else:
        difference = (sum(stan) / len(stan)) - (sum(diff) / len(diff))
        group_avg = sum(group_ans) / len(group_ans)
        pred = group_avg - difference
        if (pred < 1):
            pred = 1.00
        elif (pred > 5):
            pred = 5.00
        else:
            pred = round(pred, 2)
        Q += '\n\n이 문제에 대한 당신의 예상 답변은 ' + str(pred) + '점입니다.'
    update.message.reply_text(Q, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ENDTEST

def endtest(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s ended test.", user.first_name)
    update.message.reply_text(
        '지금까지 컴윤사봇을 이용해주셔서 감사합니다!\n테스트를 다시 진행하고 싶으시면 /start를 입력해주세요!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        '지금까지 컴윤사봇을 이용해주셔서 감사합니다!\n테스트를 다시 진행하고 싶으시면 /start를 입력해주세요!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main():
    updater = Updater('1452014249:AAF8xlpe6r3sAq0c3ZJ--HH6I5qT5ZBftQs', use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGE: [MessageHandler(Filters.regex('^(20대|30대l|40대|기타)$'), age)],
            GENDER: [MessageHandler(Filters.regex('^(남성|여성|기타)$'), gender)],
            JOB: [MessageHandler(Filters.regex('^(학생|대학원생|회사원|자영업자|전문직|기타)$'), job)],
            # INFOEND: [MessageHandler(Filters.text & ~Filters.command, infoend)],
            ASKQ1: [MessageHandler(Filters.regex('^(시작)$'), askQ1)],
            ASKQ2: [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), askQ2)],
            ASKQ3: [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), askQ3)],
            PREDQ1: [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), predQ1)],
            PREDQ2: [MessageHandler(Filters.regex('^(다음)$'), predQ2)],
            PREDQ3: [MessageHandler(Filters.regex('^(다음)$'), predQ3)],
            ENDTEST: [MessageHandler(Filters.regex('^(다음)$'), endtest)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
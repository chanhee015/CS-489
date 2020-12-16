import sys
import pandas as pd
import csv
import time
import logging
import random

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ConversationHandler, MessageHandler, Updater, Filters

import dilemma
# 1. 사용자가 /teststart로 test시작.
# 2. 이 id를 확인 (id를 받아오는 것까지는 됐는데 test를 실행한 사람 id를 받아오는건 아직 안됨)
# 3. 해당 id가 'info.csv'에 있는지 확인. 없으면 3-1로, 있으면 3-2로. (csv 파일 형식: ['id', 'age', 'gender', 'job']) (성공)
# 3-1. 없으면 age, gender, job을 물어본 후 저장. 3-2로 감. (성공)
# 3-2. age, gender, job을 확인 후 해당하는 csv 파일로 감. (20_male_student 이런식)
# 4. 질문하기 및 그 질문에 대한 평균을 보여주기 (성범) -- 답변이 없었던 질문인데 이게 조합되어 만든 질문일 경우에는 그 평균도 함께 보여줄 수 있어야 함.
# 5. 해당 질문과 그에 대한 답변을 csv에 저장. (ex. '20_male_student.csv'에 [딜레마, 점수] 형식으로 저장 -- 저장 방식은 딜레마 어떻게 조합 및 제공하냐에 따라 달라짐)


data_file_name = 'answers/20대_남성_학생.csv'
data_file = open(data_file_name, 'a', encoding='utf-8', newline='')

for i in range (500):
    qnum = random.randrange(0, 13)
    id = 1111
    point = random.randrange(1, 6)
    csv.writer(data_file).writerow([qnum, id, point])
data_file.close()
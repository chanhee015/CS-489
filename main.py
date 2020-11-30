import sys
import bot_skeleton
import telegram
import pandas as pd
import csv

# 1. 사용자가 /teststart로 test시작. (성범 완료 시 구현 바로 가능)
# 2. 이 id를 확인 (id를 받아오는 것까지는 됐는데 test를 실행한 사람 id를 받아오는건 아직 안됨)
# 3. 해당 id가 'info.csv'에 있는지 확인. 없으면 3-1로, 있으면 3-2로. (csv 파일 형식: ['id', 'age', 'gender', 'job']) (성공)
# 3-1. 없으면 age, gender, job을 물어본 후 저장. 3-2로 감. (성공)
# 3-2. age, gender, job을 확인 후 해당하는 csv 파일로 감. (20_male_student 이런식)
# 4. 질문하기 및 그 질문에 대한 평균을 보여주기 (성범) -- 답변이 없었던 질문인데 이게 조합되어 만든 질문일 경우에는 그 평균도 함께 보여줄 수 있어야 함.
# 5. 해당 질문과 그에 대한 답변을 csv에 저장. (ex. '20_male_student.csv'에 [딜레마, 점수] 형식으로 저장 -- 저장 방식은 딜레마 어떻게 조합 및 제공하냐에 따라 달라짐, 성범이 코딩하면서 결정)

def get_info(id): # 3번에 해당하는 함수.
    info_exist = False
    info_file = open('info.csv', 'r', encoding='utf-8', newline='')
    reader = csv.reader(info_file, delimiter=',')
    for row in reader:
        if (row[0] == id):
            info_exist = True
            age = row[1]
            gender = row[2]
            job = row[3]
    info_file.close()

    if (info_exist):
        return age, gender, job
    else:
        ###### ASK ABOUT INFO & RETURN ##### SHOULD BE IMPLEMENTED!!!
        # info_file = open('info.csv', 'a', encoding='utf-8', newline='')
        # csv.writer(info_file).writerow([id, age, gender, job])
        # info_file.close()
        # return age, gender, job
        pass





# def proc_stop(bot, update):
#     cs489.sendMessage('End of test.')
#     cs489.stop()
#
# def ethics_test(bot, update):
#     cs489.sendMessage('Starting Ethics test')
#     test_function() TELEGRAM_TOKEN = '1452014249:AAF8xlpe6r3sAq0c3ZJ--HH6I5qT5ZBftQs'
# cs489 = bot_skeleton.Ethicsbot()
# cs489.add_handler('test', ethics_test)
# cs489.start()
#

TELEGRAM_TOKEN = '1452014249:AAF8xlpe6r3sAq0c3ZJ--HH6I5qT5ZBftQs'

cs489 = telegram.Bot(token=TELEGRAM_TOKEN)
updates = cs489.getUpdates()
# print(updates.message)
# chat_id = updates[-1].message.chat_id
# cs489.sendMessage(chat_id=chat_id, text='201125')
# for u in updates :   # 내역중 메세지를 출력합니다.
#     print(u.message.chat_id, u.message.text)
# abc = pd.DataFrame([, ], columns=['id', 'age', 'gender', 'job'])
# abc.to_csv('test.csv', mode='a', header=False)



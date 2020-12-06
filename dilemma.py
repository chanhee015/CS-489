import csv
import random

# note1
# globalvariable
q_1st = []
q_2nd = []
adder = 0


# note2
# 1st_function
# 한 사람당 1번째로 물어볼 질문 유형별로 한세트 (3개), 2번째로 물어볼 질문 유형별로 한 세트 (3개) list로 만드는 함수, 1번째는 평균값 제공, 2번째는 우리가 예상치 먼저 제공

def ran_qlist():
    # for문시작
    for i in range(3):
        if i == 0:
            numb = 0
            adder = 7
        elif i == 1:
            numb = 8
            adder = 7
        else:
            numb = 16
            adder = 9

        ran_num = random.randint(numb, numb + adder)
        q_1st.append(ran_num)

        for j in range(1):
            while ran_num in q_1st:
                ran_num = random.randint(numb, numb + adder)
            q_2nd.append(ran_num)
    # for문끝
    return q_1st, q_2nd


# note3
# globalvariable
dil = []

# dilema csv 읽어와서 dilema 부분만 저장
# dil 은 dilema가 담긴 list

with open('dilema.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        dil.append(row[2])


# note4
# 2nd_function
# 숫자 넣으면 번호에 따라서 딜레마 return
def q_out(z):
    return dil[z]


# note5
# 성별,나이대,직업군에 따라서 적당히 그룹 결정짓고 그 그룹별로 list다 만들어야함.
# db가 없어서 예시로 만든 부분
M2S = []
with open('20s_Male_Student.csv', 'r') as f:
    read = csv.reader(f)
    for row in read:
        M2S.append([row[0], row[1], row[2]])


# note6
# 3rd_function
# 딜레마번호, 사람 유형(list이름으로) input으로 넣으면 그 집단의 해당 질문에 대한 평균 return
# x가 문제번호, L이 사람 유형의 list
def qavg(x, L):
    M = []
    for i in range(len(L)):
        if int(L[i][0]) == x:
            M.append(int(L[i][1]))
    if len(M) != 0:
        AVG = (sum(M, 0.0) / len(M))
        RAVG = round(AVG, 2)
    else:
        return "해당 문제에 대한 데이터가 없어, 평균을 구할 수 없습니다."
    return RAVG


# note7
# globalvariable
peo_ans = dict()


# 4th function
# 어떤 유형의 질문에 대해 한 사람이 대답한 값과, 그 집단의 평균 사이의 편차를 구해주는 함수.
# idd는 그사람 id, x는 문제번호, L은 그 사람의 유형 list
# 대답 한 번 받을 때마다 csv에 저장하고, 아래의 diff 함수 실행해줘야함.

def diff(x, L, idd):
    N = []
    dif = 0.0
    if idd in peo_ans:
        N = peo_ans[idd]
    else:
        peo_ans[idd] = N

    avgg = qavg(x, L)

    for i in range(len(M2S)):
        if int(M2S[i][0]) == x:
            if str(M2S[i][2]) == str(idd):
                dif = float(M2S[i][1]) - avgg
                N.append(dif)
    return N


# note8
# 5th function
# 4th function에서 얻은 list를 바탕으로 해당 문제에 대한 예상 답변 도출

def pred(x, L, idd):
    avgg = qavg(x, L)
    cate = 0

    if x < 8:
        cate = 0
    elif 8 <= x and x < 16:
        cate = 1
    else:
        cate = 2

    P = peo_ans[idd]
    differ = P[cate] + avgg
    pre = round(differ)
    if 0 < pre and pre < 6:
        return pre
    elif pre < 1:
        return 1
    else:
        return 5
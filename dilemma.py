import csv
import random

peo_ans = dict()
M2S = []

# Choose random Qs. 3 each. Total 6. Returns as Q number.
def ran_qlist():
    q_ask = []  # Q to ask
    q_pred = []  # Q to pred
    adder = 0

    for i in range(3):
        if i == 0:
            numb = 0
            adder = 3
        elif i == 1:
            numb = 4
            adder = 3
        else:
            numb = 8
            adder = 4

        ran_num = random.randint(numb, numb + adder)
        q_ask.append(ran_num)

        while ran_num in q_ask:
            ran_num = random.randint(numb, numb + adder)
        q_pred.append(ran_num)

    return q_ask + q_pred

# Function to return dilemma with number z.
def q_out(z):
    dil = []
    with open('dilema.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            dil.append(row[2])
    return dil[z]

# with open('20s_Male_Student.csv', 'r') as f:
#     read = csv.reader(f)
#     for row in read:
#         M2S.append([row[0], row[1], row[2]])

# returns difference between person id and group L. x is Q number.
def diff(x, id, L):
    N = []
    dif = 0.0
    if id in peo_ans:
        N = peo_ans[id]
    else:
        peo_ans[id] = N

    avgg = q_avg(x, L)

    for i in range(len(M2S)):
        if int(M2S[i][0]) == x:
            if str(M2S[i][2]) == str(id):
                dif = float(M2S[i][1]) - avgg
                N.append(dif)

    return N

# Gives predicted points based on list from function diff.
def pred(x, L, id):
    avgg = q_avg(x, L)
    cate = 0

    if x < 8:
        cate = 0
    elif 8 <= x and x < 16:
        cate = 1
    else:
        cate = 2

    P = peo_ans[id]
    differ = P[cate] + avgg
    pre = round(differ)
    if 0 < pre and pre < 6:
        return pre
    elif pre < 1:
        return 1
    else:
        return 5

if __name__ == '__main__':
    print(q_out(1))
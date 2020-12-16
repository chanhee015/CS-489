import sys
import csv

def gen_files():
    age = ['20대', '30대', '40대', '기타']
    gender = ['남성', '여성', '기타']
    job = ['학생', '대학원생', '회사원', '자영업자', '전문직', '기타']

    info_file = open('info.csv', 'a')
    info_file.close()

    for i in age:
        for j in gender:
            for k in job:
                file_name = 'answers/' + i + '_' + j + '_' + k + '.csv'
                gen_file = open(file_name, 'a')
                gen_file.close()

if __name__ == '__main__':
    gen_files()
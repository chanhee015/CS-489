import sys
import csv

def gen_files():
    age = ['20s', '30s', '40s', 'Others']
    gender = ['Male', 'Female', 'Others']
    job = ['Student', 'Graduate student', 'Employee', 'Self-owner', 'Specialized', 'Others']

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
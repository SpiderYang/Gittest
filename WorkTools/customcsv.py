#/usr/bin/env python
#coding:utf-8
import csv
import random
import string
import sys
import os,uuid

class generate_csv(object):
    def __init__(self,filename,d,size):
        self.filename = filename
        self.d = d
        self.size = size
        self.delimiter = string.punctuation + '\n' + '\r'
        self.all = string.printable
    def gen_all_letter(self):
        with open(self.filename,'wb') as f:
            csvwriter = csv.writer(f,delimiter=self.d)
            while f.tell() < self.size:
                csvwriter.writerow([random.choice(string.letters) for i in range(len(string.letters))])

    def gen_printable(self):
        with open(self.filename,'wb') as f:
            csvwriter = csv.writer(f,delimiter=self.d)
            while f.tell() < self.size:
                csvwriter.writerow([random.choice(string.printable) for i in range(len(string.printable))])


if __name__ == '__main__':
    filename = raw_input('Input Filename:\n ')
    if not filename:
        if not os.path.isdir('/home/csvmake'):
            os.makedirs('/home/csvmake')
        filename = '/home/csvmake' + uuid.uuid4().hex + '.csv'
    try:
        delimiter = raw_input('Input delimiter:\n')
    except:
        delimiter = ','
    try:
        size = int(raw_input('Input file size:\n'))
    except:
        size = 10000
    try:
        types = int(raw_input('select method to generate_csv\n (1,(2,)'))
    except:
        types = 1
    ins = generate_csv(filename,delimiter,size)
    if types == 1:
        ins.gen_all_letter()
    else:
        ins.gen_printable()

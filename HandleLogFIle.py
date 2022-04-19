import linecache,os,numpy as np,re
from collections import defaultdict,Counter
import os
import pandas as pd

test_name_dict = {}
signal_list = []
log_file_path = r'D:\海图微\HT50A\HT50A\HT50A\CW\10125AE'
pattern1 = re.compile(r'(TCNT#)\s*[0-9](\s*)(SITE#)(\s*)', re.I)
pattern2 = re.compile(r'-------------------', re.I)


def LogFile():
    write_flag = False
    # Follow Code: get all files name and file count
    file_name_list = os.listdir(log_file_path)
    file_counter = len(file_name_list)
    # Follow Code: open file and handle
    for i in range(file_counter):
        file_path = log_file_path + '\\' + file_name_list[i]
        fp = open(file_path,'rb')
        # print(len(fp.readlines()))
        # Follow Code: get line count
        count = -1
        for count, line in enumerate(open(file_path, 'rU')):
            pass
        count += 1
        # Follow Code: read line information
        for line_data in range(count):
            text = linecache.getline(file_path, line_data)
            if re.search(pattern1, text):
                write_flag = True
                line_target = line_data + 1
                for line_target in range(line_target,count):
                    text = linecache.getline(file_path, line_target)
                    text.split()
                    print(text)
                    pf1 = pd.DataFrame(columns=text.split())
                    print(pf1)
                    pass
            # if write_flag == True:
            #     text = linecache.getline(file_path, line_data)
            #
            #     print(text)

        fp.close()
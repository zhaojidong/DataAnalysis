import linecache,os,numpy as np,re
from collections import defaultdict,Counter
import os,sys
import pandas as pd

test_name_dict = {}
signal_list = []
log_file_path = r'D:\Python\Project\DataAnalysis\1009LAE0039'
pattern1 = re.compile(r'(TCNT#)\s*[0-9](\s*)(SITE#)(\s*)', re.I)
pattern2 = re.compile(r'-------------------', re.I)


def LogFile():
    pd.set_option('display.width', None)

    # Follow Code: get all files name and file count
    file_name_list = os.listdir(log_file_path)
    file_total = len(file_name_list)
    # Follow Code: open file and handle
    for i in range(file_total):
        file_path = log_file_path + '\\' + file_name_list[i]
        fp = open(file_path,'rb')
        # Follow Code: get line total sum
        count = -1
        for count, line in enumerate(open(file_path, 'r')):
            pass
        count += 1
        # Follow Code: read line information
        for line_data in range(count):
            text = linecache.getline(file_path, line_data)
            # Follow Code: Find the title's line
            if re.search(pattern1, text):
                line_target = line_data + 2
                title = linecache.getline(file_path, line_data + 1)
                # Follow Code: Title, convert to list
                title_list = title.split()
                title_len = len(title_list)
                execute_once = True
                for line_target in range(line_target, count):
                    text = linecache.getline(file_path, line_target)
                    # split according to signal space
                    line = re.split(r"[ ]+", text)
                    # delete '\n':strip() used for \n and space defaulted
                    line = [x.strip() for x in line]
                    # merger the unit with before data
                    for index,value in enumerate(line):
                        if value == 'nV' or value == 'uV' or value == 'mV' or value == 'V' \
                           or value == 'nA' or value == 'uA' or value == 'mA' or value == 'A':
                            line[index-1] = line[index-1] + line[index]
                            del line[index]
                    # list max length, append 'None' to
                    for add_none_count in range(title_len-len(line)):
                        line.append('None')
                    # Follow Code: Add the end label to the pandas dataframe
                    line_end = ['-']
                    line_end = line_end * title_len
                    line_end[0] = '-End of data-'
                    if str(line[0]).isdigit():
                        if execute_once:
                            execute_once = False
                            NewList = [[x] for x in line]
                            pd_dict = dict(zip(title_list,NewList))
                            # print(pd.DataFrame(pd_dict, index=[0]))
                        else:
                            line_count = 0
                            for key in title_list:
                                pd_dict[key] = pd_dict.get(key,[]) + [line[line_count]]
                                line_count = line_count + 1
                                if line_count > len(line)-1:
                                    break
                break
        final_pd = pd.DataFrame(pd_dict)
        final_pd.loc[len(final_pd)] = line_end
        return final_pd
        fp.close()
        break


def tryyyyy():
    dicttry = {'qaz':['q','a','z'],'wsx':['w','s','x']}
    new_pd_dict = pd.DataFrame(dicttry)
    print(new_pd_dict)


if __name__ == '__main__':
    LogFile()
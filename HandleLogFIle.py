import linecache, os, re, openpyxl, glovar as glv
from collections import defaultdict, Counter
import os
import pandas as pd
import numpy as np

import CreatFile

test_name_dict = {}
signal_list = []
log_file_path = r'D:\Python\Project\DataAnalysis\1009LAE0039'
pattern1 = re.compile(r'(TCNT#)\s*[0-9](\s*)(SITE#)(\s*)', re.I)  # the TCNT as the beginning
pattern2 = re.compile(r'-------------------', re.I)
pattern3 = re.compile(r'AnalysisData', re.I)
pattern4 = re.compile(r'(_FAIL_)', re.I)

pat_Title = re.compile(r'(NO Site(\s+)Result(\s+)TestName)', re.I)
pat_TCNT = re.compile(r'(TCNT#)\s*[0-9](\s*)(SITE#)(\s*)', re.I)
pat_End = re.compile(r'(Site(\s+)Fail(\s+)Total(\s+)Cate(\s+)Bin(\s+)XCoord(\s+)YCoord)', re.I)
pat_AnalysisData = re.compile(r'(AnalysisData_)', re.I)
pat_Over = re.compile(r'-------------------', re.I)

find_fail_str = '_FAIL_'
output_file_path = '.\Out'
title_append = ['CheckStatus']
gs = glv.global_string()

# traverse all log files, generate pandas
def ParseLogFile():
    log_file_list = glv.selected_file_list
    files_num = len(glv.selected_file_list)
    pd.set_option('display.width', None)
    # Follow Code: get all files name and file count
    file_name_list = os.listdir(log_file_path)
    file_total = len(file_name_list)
    TNCT = []
    dut_num = 0
    execute_once = True
    for f_num in range(files_num):
        fp = open(log_file_list[f_num], 'rb')
        # Follow Code: get line total sum
        count = -1
        for count, line in enumerate(open(log_file_list[f_num], 'r')):
            pass
        count += 1
        # Follow Code: read line information
        execute_once_2 = True
        pd_dict = {}
        title_len = 0
        title_list = []
        got_title = False
        execute_file = True
        finish_one_flag = False
        for line_data in range(count):
            text = linecache.getline(log_file_list[f_num], line_data)
            # Follow Code: Find the title's line
            if re.search(pat_Title, text) and execute_file:
                info_list = glv.extractNum2list(linecache.getline(log_file_list[f_num], line_data-1))
                TNCT.append(info_list[0])
                SITE = info_list[1]
                title_list = linecache.getline(log_file_list[f_num], line_data).split()
                title_list.extend(title_append)
                glv.title_pd_dict = title_list
                title_len = len(title_list)
                got_title = True
                continue
            if got_title:
                # split according to signal space
                line = re.split(r"[ ]+", text)
                # delete '\n':strip() used for \n and space defaulted
                line = [x.strip() for x in line]
                # merger the unit with before data
                for index, value in enumerate(line):
                    if value == 'nV' or value == 'uV' or value == 'mV' or value == 'V' \
                            or value == 'nA' or value == 'uA' or value == 'mA' or value == 'A':
                        line[index - 1] = line[index - 1] + line[index]
                        del line[index]
                # list max length, append 'None' to
                for add_none_count in range(title_len - len(line)):
                    line.append('None')
                # line_end[2] = file_name_info[1]  # DUT PASS or FAIL
                if re.search(pat_Over, text) is None:
                    if execute_once:
                        execute_once = False
                        NewList = [[x] for x in line]
                        pd_dict = dict(zip(title_list, NewList))
                    else:
                        line_count = 0
                        for key in title_list:
                            if str(line[0]).isdigit():  # NO. is digit, and Result is alpha
                                pd_dict[key] = pd_dict.get(key, []) + [line[line_count]]
                                line_count += 1
                            elif re.search(pat_AnalysisData, text):
                                AnalysisData_item = text.split()[:]  # value copy to list, not list copy to list
                                AnalysisData_item[0] = 999
                                AnalysisData_item[1] = 0
                                AnalysisData_item[2] = text.split()[-1] == '1' and 'PASS' or 'FAIL'
                                AnalysisData_item[3] = str(text.split()[0])
                                AnalysisData_item.extend(['-']*(title_len-len(AnalysisData_item)))
                                pd_dict[key] = pd_dict.get(key, []) + [AnalysisData_item[line_count]]
                                line_count += 1
                if re.search(pat_End, text):  # find the end line, and fill some information(test time)
                    TestTime = re.findall(r"[(](.*?)[)]", linecache.getline(log_file_list[f_num], line_data))  # get the string in the parentheses, it is test time
                    end_line_list = linecache.getline(log_file_list[f_num], line_data + 2).split()
                    end_line_list.insert(0, glv.end_label)  # '-EOL-'
                    end_line_list.append(TestTime[0])
                    end_line_list.extend(['-'] * (title_len - len(end_line_list)))
                    for each in zip(end_line_list, pd_dict):
                        ele, key = each
                        pd_dict[key].append(ele)
                    line_count += 1
                    dut_num += 1
                    finish_one_flag = True
            if finish_one_flag:
                logs_pd = pd.DataFrame(pd_dict)
                finish_one_flag = False
                if execute_once_2:
                    tree_pd = logs_pd
                    glv.single_dut_row = tree_pd.shape[0]
                    execute_once_2 = False
        if f_num == 0:
            final_pd = logs_pd
        else:
            final_pd = pd.concat([final_pd, logs_pd], axis=0)
        fp.close()
    # file_pd.to_csv(r'D:\Python\Project\DataAnalysis\first_pd.txt')
    # logs_pd.to_csv(r'D:\Python\Project\DataAnalysis\final_pd.txt')
    glv.final_df = final_pd
    glv.dut_count = dut_num
    print('dut_count:', glv.dut_count)
    return tree_pd, final_pd, file_name_list, file_total


def handle_FinalPd4tree():
    target_df = glv.final_df  # dataframe
    # target_tree = {'OS_NEG': ['CH_VCOMS_B1', 'CH_VCOMS_T1', 'CH_VREFN_B1', 'CH_VREFN_T1', 'CH_VREFP_B1', 'CH_VREFP_T1', 'CH_VRPGA_B1', 'CH_VRPGA_T1', 'CH_VDDCL1', 'CH_RSH1', 'CH_GRSTH1', 'CH_TX2H1', 'CH_TX1H1', 'SA', 'SYSSTBN', 'SYSRSTN', 'VCP2', 'VIREF', 'SDO', 'CSN', 'SCK', 'SDI', 'HSYNC', 'VSYNC', 'DTSTR0', 'DTSTR1', 'DTSTR3', 'DTSTR4', 'TOUT0', 'TOUT1', 'TOUT2', 'ATST0', 'ATST1', 'ATST2', 'RCK2', 'TRGEXP', 'MSTSLV', 'TSG2_config.TSG2_config', 'TSG2.TSG2', 'compare', 'TSG2.TSG2', 'compare'], 'TSG2_TEST': ['CH_VCOMS_B1', 'CH_VCOMS_T1', 'CH_VREFN_B1', 'CH_VREFN_T1', 'CH_VREFP_B1', 'CH_VREFP_T1', 'CH_VRPGA_B1', 'CH_VRPGA_T1', 'CH_VDDCL1', 'CH_RSH1', 'CH_GRSTH1', 'CH_TX2H1', 'CH_TX1H1', 'SA', 'SYSSTBN', 'SYSRSTN', 'VCP2', 'VIREF', 'SDO', 'CSN', 'SCK', 'SDI', 'HSYNC', 'VSYNC', 'DTSTR0', 'DTSTR1', 'DTSTR3', 'DTSTR4', 'TOUT0', 'TOUT1', 'TOUT2', 'ATST0', 'ATST1', 'ATST2', 'RCK2', 'TRGEXP', 'MSTSLV', 'TSG2_config.TSG2_config', 'TSG2.TSG2', 'compare', 'TSG2.TSG2', 'compare']}
    target_tree = glv.tree_checked
    finish_once = False
    for index, row in target_df.iterrows():
        for key, values in target_tree.items():
            if isinstance(values, list):
                for value in values:
                    if key == target_df.at[index, str(gs.TestName)] and value == target_df.at[index, str(gs.Signal)]:
                        target_df.at[index, str(gs.CheckStatus)] = str(glv.Checked)
                        finish_once = True
                        break
            if finish_once:
                finish_once = False
                break
        if index == glv.single_dut_row:
            break
    glv.marked_df = target_df
    # target_df.to_csv(r'D:\Python\Project\DataAnalysis\final_pd.txt')


if __name__ == '__main__':
    # a,b = HT_DataAnalysis_UI.traverse_tree()
    # creat_report_excel()
    ParseLogFile()
    handle_FinalPd4tree()
    CreatFile.CreatExcel_VP_log()
    pass


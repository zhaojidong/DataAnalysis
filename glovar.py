import pandas as pd
"""
The global variable
"""
#NO,Site,Result,TestName,Signal,Measure,LowLimit,HighLimit,Force,CheckStatus
selected_file_list = ()  # the been selected file list
# selected_file_list = [r'D:\Python\Project\DataAnalysis\0001_FAIL_datalog_20220402170730.txt']
end_label = '-EOL-'
tree_checked = {}
final_df = pd.DataFrame()
title_pd_dict = {}
single_dut_row = 0
marked_df = pd.DataFrame()
output_file_path = '.\Out'
dut_count = 0
shift_count = 0
checked_count_from_tree = 0
Checked = 'Checked'
"""
The global function
Include some small function to deal string...
"""
# get digital from string
def extractNum2list(str1):
    num_list_new = []  # store the result
    a = ''
    for i in str1:
        if str.isdigit(i):
            a += i
        else:
            a += " "
    num_list = a.split(" ")
    for i in num_list:
        try:
            if int(i) >= 0:
                num_list_new.append(int(i))
            else:
                pass
        except:
            # print('Something is Wrong!')
            pass
    return num_list_new

"""
global class
"""
name_list = ['NO', 'Site', 'Result', 'TestName', 'Signal', 'Measure', 'LowLimit', 'HighLimit', 'Force', 'CheckStatus']
class global_string:
    def __init__(self):
        self.NO = str()
        self.Site = str()
        self.Result = str()
        self.TestName = int()
        self.Signal = str()
        self.Measure = str()
        self.LowLimit = str()
        self.HighLimit = int()
        self.Force = str()
        self.CheckStatus = str()

        self.setValue('NO',
                      'Site',
                      'Result',
                      'TestName',
                      'Signal',
                      'Measure',
                      'LowLimit',
                      'HighLimit',
                      'Force',
                      'CheckStatus')

    def setValue(self, NO, Site, Result, TestName, Signal, Measure, LowLimit, HighLimit, Force, CheckStatus):
        self.NO = NO
        self.Site = Site
        self.Result = Result
        self.TestName = TestName
        self.Signal = Signal
        self.Measure = Measure
        self.LowLimit = LowLimit
        self.HighLimit = HighLimit
        self.Force = Force
        self.CheckStatus = CheckStatus











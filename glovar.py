import pandas as pd, re

"""
# debug using
"""
final_path = r'C:\007\PythonProject\Ref_Data\DataAnalysis\Out\final_pd.txt'
t = 0
s = 0
"""
The global variable
"""
# NO,Site,Result,TestName,Signal,Measure,LowLimit,HighLimit,Force,CheckStatus
selected_file_list = ()  # the been selected file list
# selected_file_list = [r'D:\Python\Project\DataAnalysis\0001_FAIL_datalog_20220402170730.txt']
end_label = '-EOL-'
tree_checked = {}
title_pd_dict = {}
log_row = 0
log_col = 0
output_file_path = r'C:\007\PythonProject\Ref_Data\DataAnalysis\Out'
dut_count = 0
shift_count = 0
checked_count_from_tree = 0
final_df = pd.DataFrame()
marked_df = pd.DataFrame()
tree_df = pd.DataFrame()
# SA result
R_yield = 0
DUT_NO = []
DUT_Val = []
DUT_math = {}  # Average , Median, Variance, Standard deviation, Max, Min
# DUT_math_key = ['Ave', 'Med', 'Var', 'St_dev', 'Max', 'Min']

# The principle of:
# Case insensitive
# unit:nV, uV, mV, V, nA, uA, mA, A, M, MHZ, K, KHZ, R
pat_unit = re.compile(r'(NO Site(\s+)Result(\s+)TestName)', re.I)
"""
global class---dataframe title
"""
name_list = ['NO', 'Site', 'Result', 'TestName', 'Signal', 'Measure', 'LowLimit', 'HighLimit', 'Force',
             'CheckStatus', 'PASS_Count', 'Fail_Count', 'unit']
class global_str:
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
        self.PASS_Count = str()
        self.Fail_Count = str()
        self.Unit = str()

        self.setValue('NO', 'Site', 'Result', 'TestName', 'Signal', 'Measure', 'LowLimit', 'HighLimit', 'Force',
                      'CheckStatus', 'PASS_Count', 'Fail_Count', 'unit')

    def setValue(self, NO, Site, Result, TestName, Signal, Measure, LowLimit, HighLimit, Force, CheckStatus,
                 PASS_Count, Fail_Count, Unit):
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
        self.PASS_Count = PASS_Count
        self.Fail_Count = Fail_Count
        self.Unit = Unit

    # global class---global string
class global_status_str:
    def __init__(self):
        self.Checked = str()
        self.PASS = str()
        self.FAIL = str()

        self.setValue('Checked', 'PASS', 'FAIL')

    def setValue(self, Checked, PASS, FAIL):
        self.Checked = Checked
        self.PASS = PASS
        self.FAIL = FAIL


# global class---global string
class global_table_str:
    def __init__(self):
        self.none = str()
        self.Histogram = str()
        self.Curve_chart = str()
        self.Normal_distribution = str()

        self.Excel_VP = str()

        self.setValue('None', 'Histogram', 'Curve chart', 'Normal Distribution',
                      'VP')

    def setValue(self, none, Histogram, Curve_chart, Normal_distribution,
                 VP):
        self.none = none
        self.Histogram = Histogram
        self.Curve_chart = Curve_chart
        self.Normal_distribution = Normal_distribution

        self.Excel_VP = VP


# Average , Median, Variance, Standard deviation, Max, Min
class global_math:
    def __init__(self):
        self.Ave = str()
        self.Med = str()
        self.Var = str()
        self.St_dev = str()
        self.Max = str()
        self.Min = str()

        self.setValue('Ave', 'Med', 'Var', 'St_dev', 'Max', 'Min')

    def setValue(self, Ave, Med, Var, St_dev, Max, Min):
        self.Average = Ave
        self.Median = Med
        self.Variance = Var
        self.St_dev = St_dev
        self.Max = Max
        self.Min = Min


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
            pass
    return num_list_new


def extractUnit7UnifyValue(data_l):
    unit_l = []
    for d in range(data_l):
        unit_l[d] = ''.join([data_l[d] for data_l[d] in str if data_l[d].isalpha()])

    unit_len = len(unit_l)
    set(unit_l)
    if len(set(unit_l)) == 1:

    for u in range(unit_l):

        pass
if __name__ == '__main__':
    # data = ['1.2462V', '900.0000mV', '1.3000V']
    # extractUnit7UnifyValue(data)
    a = [22, 22, 22, 22]
    print(list(set(a)))
    b = len(set(a))
    if b > 1:
        print("重复")






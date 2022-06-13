import pandas as pd, re
from collections import Counter
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
WaveForm_pd = pd.DataFrame()
# SA result
R_yield = 0
DUT_NO = []
DUT_Val = []
DUT_math = {}  # Average , Median, Variance, Standard deviation, Max, Min
# DUT_math_key = ['Ave', 'Med', 'Var', 'St_dev', 'Max', 'Min']

# The principle of:
# Case insensitive
# unit:nV, uV, mV, V, nA, uA, mA, A, M, MHZ, K, KHZ, R
all_units = ['nV', 'uV', 'mV', 'V', 'nA', 'uA', 'mA', 'A', 'HZ', 'M', 'MHZ', 'K', 'KHZ', 'R']
pat_unit = re.compile(r'(NO Site(\s+)Result(\s+)TestName)', re.I)
plot_fmt_color = ['b', 'r', 'c', 'm', 'g', 'y', 'k', 'tan', 'gold', 'grey', 'peru']
error_message = ''
"""
global class---dataframe title
"""
name_list = ['NO', 'Site', 'Result', 'TestName', 'Signal', 'Measure', 'LowLimit', 'HighLimit', 'Force',
             'CheckStatus', 'PASS_Count', 'Fail_Count', 'Unit']
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
                      'CheckStatus', 'PASS_Count', 'Fail_Count', 'Unit')

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

glv_gs = global_str()
    # global class---global string
class global_status_str:
    def __init__(self):
        self.Checked = str()
        self.PASS = str()
        self.FAIL = str()
        self.NaN = str()

        self.setValue('Checked', 'PASS', 'FAIL', 'NaN')

    def setValue(self, Checked, PASS, FAIL, NaN):
        self.Checked = Checked
        self.PASS = PASS
        self.FAIL = FAIL
        self.NaN = NaN

glv_gss = global_status_str()
# global class---global string
class global_table_str:
    def __init__(self):
        self.none = str()
        self.Histogram = str()
        self.Curve_chart = str()
        self.Normal_distribution = str()
        self.Scatter_diagram = str()
        self.Line_chart = str()
        self.Box_plots = str()

        self.Excel_VP = str()

        self.setValue('None', 'Histogram', 'CurveChart', 'NormalDistribution', 'ScatterDiagram', 'LineChart', 'BoxPlots',
                      'VP')

    def setValue(self, none, Histogram, Curve_chart, Normal_distribution, Scatter_diagram, Line_chart, Box_Plots,
                 VP):
        self.none = none
        self.Histogram = Histogram
        self.Curve_chart = Curve_chart
        self.Normal_distribution = Normal_distribution
        self.Scatter_diagram = Scatter_diagram
        self.Line_chart = Line_chart
        self.Box_plots = Box_Plots

        self.Excel_VP = VP


# Average , Median, Variance, Standard deviation, Max, Min
class global_math:
    def __init__(self):
        self.Average = str()
        self.Median = str()
        self.Variance = str()
        self.St_dev = str()
        self.Max = str()
        self.Min = str()

        self.setValue('Average', 'Median', 'Variance', 'St_dev', 'Max', 'Min')

    def setValue(self, Average, Median, Variance, St_dev, Max, Min):
        self.Average = Average
        self.Median = Median
        self.Variance = Variance
        self.St_dev = St_dev
        self.Max = Max
        self.Min = Min

glv_gm = global_math()
SA_pd_col = [glv_gs.TestName, glv_gs.Signal, glv_gs.LowLimit, glv_gs.HighLimit, glv_gs.CheckStatus,
             glv_gs.Unit, glv_gm.Average, glv_gm.Median,glv_gm.Variance, glv_gm.St_dev, glv_gm.Max, glv_gm.Min]
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
    unit_l = [0]*len(data_l)
    unit_class = [0] * len(data_l)
    digital_l = [0]*len(data_l)
    final_res = [glv_gss.NaN]*len(data_l)
    error_flag = False
    for d in range(len(data_l)):
        unit_l[d] = ''.join(re.findall(r'[A-Za-z]', data_l[d]))
        unit_class[d] = data_l[d][-1]
        digital_l[d] = data_l[d][0:(len(data_l[d])-len(unit_l[d]))]
    if len(set(unit_class)) != 1 and '0' not in unit_class:
        print(unit_class)
        error_message = 'The units are different, so it cannot be counted!!!'
        error_flag = True
        print(error_message)
        unit = glv_gss.NaN
        return final_res, error_flag, unit
    else:
        unit = unit_l[0]
        if unit not in all_units:
            unit = glv_gss.NaN
        else:
            unit = unit_l[0]
    try:
        digital_l = list(map(lambda x: float(x), digital_l))  # convert string to float
    except:
        print(digital_l)
        print('ValueError: Could not convert string to float')
        error_flag = True
        return final_res, error_flag, unit
    if len(set(unit_l)) == 1:
        # all units are the same, just extract the digital
        final_res = digital_l
    else:
        # all units are different, Unify the Value
        result = Counter(unit_l)  # Number of unit occurrences
        res = max(result, key=lambda x: result[x])  # find the max number of unit base on the last result
        if 'm' in res:
            for d in range(len(data_l)):
                unit_l[d] = ''.join(re.findall(r'[A-Za-z]', data_l[d]))
                if res == unit_l[d]:
                    final_res[d] = digital_l[d]
                elif 'u' in unit_l[d]:
                    final_res[d] = digital_l[d] / 1e3
                elif 'n' in unit_l[d]:
                    final_res[d] = digital_l[d] / 1e6
                else:
                    final_res[d] = digital_l[d] * 1e3
        elif 'u' in res:
            for d in range(len(data_l)):
                unit_l[d] = ''.join(re.findall(r'[A-Za-z]', data_l[d]))
                if res == unit_l[d]:
                    final_res[d] = digital_l[d]
                elif 'm' in unit_l[d]:
                    final_res[d] = digital_l[d] * 1e3
                elif 'n' in unit_l[d]:
                    final_res[d] = digital_l[d] / 1e3
                else:
                    final_res[d] = digital_l[d] * 1e6
        elif 'n' in res:
            for d in range(len(data_l)):
                unit_l[d] = ''.join(re.findall(r'[A-Za-z]', data_l[d]))
                if res == unit_l[d]:
                    final_res[d] = digital_l[d]
                elif 'm' in unit_l[d]:
                    final_res[d] = digital_l[d] * 1e6
                elif 'u' in unit_l[d]:
                    final_res[d] = digital_l[d] * 1e3
                else:
                    final_res[d] = digital_l[d] * 1e9
        else:
            for d in range(len(data_l)):
                unit_l[d] = ''.join(re.findall(r'[A-Za-z]', data_l[d]))
                if res == unit_l[d]:
                    final_res[d] = digital_l[d]
                elif 'm' in unit_l[d]:
                    final_res[d] = digital_l[d] / 1e3
                elif 'u' in unit_l[d]:
                    final_res[d] = digital_l[d] / 1e6
                else:
                    final_res[d] = digital_l[d] / 1e9
    return final_res, error_flag, unit


if __name__ == '__main__':
    data = ['-398.7766mV', '-406.6084mV', '-399.6171mV', '-404.3162mV']
    extractUnit7UnifyValue(data)
    # a = [22, 22, 22, 22]
    # print(list(set(a)))
    # b = len(set(a))
    # if b > 1:
    #     print("重复")






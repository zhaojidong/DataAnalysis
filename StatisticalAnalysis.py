"""
This py uesd to statistical and analysis the log data which were selected on tree widget
1.Yeild
"""
import numpy as np
import pandas as pd
from numpy import mean
from matplotlib import pyplot as plt
import matplotlib
import glovar as glv

gs = glv.global_str()
gss = glv.global_status_str()
gm = glv.global_math()


class SA:
    def __init__(self, marked_df, parent=None):  # parent=None,so the HaiTu_UI is the topmost window
        # super(self).__init__(parent)  # the super().__init__() excutes the constructor fo father, then we can use the property of father
        self.sa_mk_df = marked_df
        self.init()

    def init(self):
        self.R_Yield()
        self.handle_EverySignalData()
        pass

    # calculate the yield
    def R_Yield(self):
        fail_counts = 0
        DUT_PF = [1]*glv.dut_count
        shift_count = glv.log_row
        for index, row in self.sa_mk_df.iterrows():
            if index == glv.log_row:  # only loop the first dut's log, because it was marked
                break
            if self.sa_mk_df.at[index, str(gs.CheckStatus)] == str(gss.Checked) and sum(DUT_PF) != 0:
                for dut in range(glv.dut_count):
                    if self.sa_mk_df.at[index + dut * shift_count, str(gs.Result)] == str(gss.FAIL):
                        fail_counts += 1
                        DUT_PF[dut] = 0
                    if sum(DUT_PF) == 0:
                        break
        glv.R_yield = round((sum(DUT_PF)/len(DUT_PF)) * 100, 2)

    # plto the waveform of checked value, include ave value, min, max, median, stdev
    def plot_single_itme(self):
        DUT_Val = [0]*glv.dut_count
        DUT_PF = [1]*glv.dut_count
        shift_count = glv.log_row
        for index, row in self.sa_mk_df.iterrows():
            if index == glv.log_row:  # only loop the first dut's log, because it was marked
                break
            if self.sa_mk_df.at[index, str(gs.CheckStatus)] == str(gss.Checked) and sum(DUT_PF) != 0:
                for dut in range(glv.dut_count):
                    DUT_Val[dut] = self.sa_mk_df.at[index + dut * shift_count, str(gs.Measure)]
                break
        DUT_Val, _, _ = glv.extractUnit7UnifyValue(DUT_Val)
        glv.DUT_Val = DUT_Val
        # Average
        glv.DUT_math[gm.Average] = np.mean(DUT_Val).round(3)
        # Median
        glv.DUT_math[gm.Median] = np.median(DUT_Val).round(3)
        # Variance
        glv.DUT_math[gm.Variance] = np.var(DUT_Val).round(3)
        # Standard deviation
        glv.DUT_math[gm.St_dev] = np.std(DUT_Val).round(3)
        # Max
        glv.DUT_math[gm.Max] = round(max(DUT_Val), 3)
        # Min
        glv.DUT_math[gm.Min] = round(min(DUT_Val), 3)

        # print('glv.DUT_Val:', glv.DUT_Val)
        # print('glv.DUT_math:', glv.DUT_math)

    def handle_EverySignalData(self):
        global unit
        SA_df_copy = glv.marked_df.copy()
        SA_df = pd.DataFrame(columns=glv.SA_pd_col)
        shift_count = glv.log_row
        DUT_Val = [0]*glv.dut_count
        executed = False
        for index, row in SA_df_copy.iterrows():
            if SA_df_copy.at[index, str(gs.CheckStatus)] == gss.Checked:
                SA_df.at[index, str(gs.TestName)] = SA_df_copy.at[index, str(gs.TestName)]
                SA_df.at[index, str(gs.Signal)] = SA_df_copy.at[index, str(gs.Signal)]
                SA_df.at[index, str(gs.LowLimit)] = SA_df_copy.at[index, str(gs.LowLimit)]
                SA_df.at[index, str(gs.HighLimit)] = SA_df_copy.at[index, str(gs.HighLimit)]
                SA_df.at[index, str(gs.CheckStatus)] = SA_df_copy.at[index, str(gs.CheckStatus)]
                for dut in range(glv.dut_count):
                    DUT_num = 'DUT_' + str(glv.DUT_NO[dut])
                    SA_df.at[index, DUT_num] = SA_df_copy.at[index + dut * shift_count, str(gs.Measure)]
                    DUT_Val[dut] = SA_df_copy.at[index + dut * shift_count, str(gs.Measure)]
                # print(DUT_Val)
                try:
                    DUT_Val, error_flag, unit = glv.extractUnit7UnifyValue(DUT_Val)
                    for dut in range(glv.dut_count):
                        DUT_num = 'DUT_' + str(glv.DUT_NO[dut])
                        SA_df.at[index, DUT_num] = DUT_Val[dut]
                except:
                    print('The data or unit maybe wrong')
                    # break
                if not error_flag:
                    # Average
                    SA_df.at[index, str(gm.Average)] = np.mean(DUT_Val).round(3)
                    # Median
                    SA_df.at[index, str(gm.Median)] = np.median(DUT_Val).round(3)
                    # Variance
                    SA_df.at[index, str(gm.Variance)] = np.var(DUT_Val).round(3)
                    # Standard deviation
                    SA_df.at[index, str(gm.St_dev)] = np.std(DUT_Val).round(3)
                    # Max
                    SA_df.at[index, str(gm.Max)] = round(max(DUT_Val), 3)
                    # Min
                    SA_df.at[index, str(gm.Min)] = round(min(DUT_Val), 3)
                    # Unit
                    SA_df.at[index, str(gs.Unit)] = unit
                else:
                    # Average
                    SA_df.at[index, str(gm.Average)] = gss.NaN
                    # Median
                    SA_df.at[index, str(gm.Median)] = gss.NaN
                    # Variance
                    SA_df.at[index, str(gm.Variance)] = gss.NaN
                    # Standard deviation
                    SA_df.at[index, str(gm.St_dev)] = gss.NaN
                    # Max
                    SA_df.at[index, str(gm.Max)] = gss.NaN
                    # Min
                    SA_df.at[index, str(gm.Min)] = gss.NaN
                    # Unit
                    SA_df.at[index, str(gs.Unit)] = unit

            if index == shift_count-2:
                break
        SA_df.to_csv(glv.final_path)
        glv.WaveForm_pd = SA_df.copy()
        # print('SA_df.copy():', SA_df)





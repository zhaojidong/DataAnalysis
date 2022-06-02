"""
This py uesd to statistical and analysis the log data which were selected on tree widget
1.Yeild
"""
import numpy as np
from numpy import mean

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
        self.plot_single_itme()
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
        glv.DUT_Val = DUT_Val
        # Average
        print(DUT_Val)
        print(glv.DUT_math)
        print(str(gm.Average))
        print(np.mean(DUT_Val))
        glv.DUT_math[gm.Average] = np.mean(DUT_Val)
        # Median
        glv.DUT_math[str(gm.Median)] = np.median(DUT_Val)
        # Variance
        glv.DUT_math[str(gm.Variance)] = np.var(DUT_Val)
        # Standard deviation
        glv.DUT_math[str(gm.St_dev)] = np.std(DUT_Val)
        # Max
        glv.DUT_math[str(gm.Max)] = max(DUT_Val)
        # Min
        glv.DUT_math[str(gm.Min)] = min(DUT_Val)

        print('glv.DUT_Val:', glv.DUT_Val)
        print('glv.DUT_math:', glv.DUT_math)
    # plot the Normal distribution

import multiprocessing

import pandas as pd
from matplotlib import pyplot as plt
import matplotlib, os
import mplcursors
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngine import *
from pyecharts.charts import Bar, Page, Scatter, Boxplot, Line
from pyecharts import options as opts
matplotlib.use('QtAgg')  # 指定渲染后端。QtAgg后端指用Agg二维图形库在Qt控件上绘图。
# matplotlib.use('Qt5Agg')
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import glovar as glv
# 导入输出图片工具
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot
from multiprocessing import Process

dwf_gs = glv.global_str()
dwf_gts = glv.global_table_str()

class DrawWaveForm(FigureCanvasQTAgg):
    def __init__(self):
        # S1：Create a Figure
        self.po_annotation = []
        self.TName = None
        self.DUT_V = None
        self.WF_PD = None
        self.ax = None
        self.figs = Figure()
        # S2：Active Figure windows in the parent class
        super(DrawWaveForm, self).__init__(self.figs)  # This is essential，otherwise, the graph will not be displayed
        self.canvas = FigureCanvasQTAgg(self.figs)  # create figure canvas
        self.ax = self.figs.subplots()

    def init(self):
        self.WF_PD = glv.WaveForm_pd.copy()
        self.DUT_V = [0] * glv.dut_count
        self.TName = []# * glv.dut_count
        on_move_id = self.canvas.mpl_connect('motion_notify_event', self.on_move)
        print('on_move_id:', on_move_id)
        # plt.show()

    def showInfo(self, x, y):
        print(x, y)
        for i in range(len(x)):
            # 标注点的坐标
            point_x = x[i]
            point_y = y[i]
            point, = plt.plot(point_x, point_y, 'o', c='darkgreen')
            # 标注plt.annotate
            annotation = plt.annotate((x[i], y[i]), xy=(x[i], y[i]), size=10)
            # 默认鼠标未指向时不显示标注信息
            annotation.set_visible(False)
            self.po_annotation.append([point, annotation])


    def on_move(self, event):
        visibility_changed = False
        for point, annotation in self.po_annotation:
            should_be_visible = (point.contains(event)[0] == True)
            print(should_be_visible)
            print('point.contains(event)[0]:', point.contains(event))
            print('event:', event)
            if should_be_visible != annotation.get_visible():
                visibility_changed = True
                annotation.set_visible(should_be_visible)
        if visibility_changed:
            # plt.ion()
            # plt.draw()
            print('self.po_annotation:', self.po_annotation)
            print('1234567890')
            event.canvas.draw_idle()
            # self.canvas.flush_events()

    def CurveGraph(self):
        self.ax.cla()
        x_axis = glv.DUT_NO
        data_y = 0
        y_axis = []
        x_axis_count = 0
        for index, row in self.WF_PD.iterrows():
            x_axis_count += 1
            self.TName.append(self.WF_PD.at[index, str(dwf_gs.TestName)] + '@' + self.WF_PD.at[
                index, str(dwf_gs.Signal)])
            unit = '(' + self.WF_PD.at[index, str(dwf_gs.Unit)] + ')'
            for dut in range(glv.dut_count):
                data_y += 1
                DUT_num = 'DUT_' + str(glv.DUT_NO[dut])
                self.DUT_V[dut] = self.WF_PD.at[index, DUT_num]
                y_axis.append(self.WF_PD.at[index, DUT_num])
            point, = self.ax.plot(x_axis, self.DUT_V, glv.plot_fmt_color[index], marker='o', linestyle='-')
            self.ax.legend(self.TName, loc='upper right')
        for i in range(len(x_axis)):
            annotation = plt.annotate((x_axis[i], y_axis[i]), xy=(x_axis[i], y_axis[i]), size=10)
            # 默认鼠标未指向时不显示标注信息
            annotation.set_visible(False)
            self.po_annotation.append([point, annotation])
            # self.showInfo(x_axis, y_axis)
        # self.ax.hlines(y=1, xmin=0, xmax=2, colors="r", linestyles="dashed")  # hline和vline
        # self.ax.hlines(y=3, xmin=0, xmax=2, colors="r", linestyles="dashed")  # hline和vline
        self.ax.set_title("Curve Graph")
        self.ax.set_xlabel('DUT NO')
        self.ax.set_ylabel('Value' + unit)
        self.draw()

    def ScatterDiagram(self):
        self.ax.cla()
        x_axis = glv.DUT_NO
        for index, row in self.WF_PD.iterrows():
            self.TName.append(self.WF_PD.at[index, str(dwf_gs.TestName)] + '@' + self.WF_PD.at[
                index, str(dwf_gs.Signal)])
            unit = '(' + self.WF_PD.at[index, str(dwf_gs.Unit)] + ')'
            for dut in range(glv.dut_count):
                DUT_num = 'DUT_' + str(glv.DUT_NO[dut])
                self.DUT_V[dut] = self.WF_PD.at[index, DUT_num]
            self.ax.scatter(x_axis, self.DUT_V, c=glv.plot_fmt_color[index])
            self.ax.legend(self.TName, loc='upper right')
        self.ax.set_xlabel('DUT NO')
        self.ax.set_ylabel('Value' + unit)
        self.draw()

    def Histogram(self, x_axis, y_axis):
        # self.ax.cla()
        # self.draw()
        pass

    def BoxPlots(self):
        self.ax.cla()
        x_axis = glv.DUT_NO
        data_y = 0
        y_axis = []
        x_axis_count = 0
        DUT_V_2list = []
        for index, row in self.WF_PD.iterrows():
            DUT_V_2list.append([])
            x_axis_count += 1
            self.TName.append(self.WF_PD.at[index, str(dwf_gs.TestName)] + '@' + self.WF_PD.at[
                index, str(dwf_gs.Signal)])
            unit = '(' + self.WF_PD.at[index, str(dwf_gs.Unit)] + ')'
            for dut in range(glv.dut_count):
                data_y += 1
                DUT_num = 'DUT_' + str(glv.DUT_NO[dut])
                self.DUT_V[dut] = self.WF_PD.at[index, DUT_num]
                DUT_V_2list[index].append(self.WF_PD.at[index, DUT_num])
                y_axis.append(self.WF_PD.at[index, DUT_num])
            self.ax.legend(self.TName, loc='upper right')
        box_dict = dict(zip(self.TName, DUT_V_2list))
        box_pd = pd.DataFrame([box_dict])
        # for key, value in box_dict.items():
        bplot1 = self.ax.boxplot(DUT_V_2list,
                                 vert=True,
                                 patch_artist=True, labels=self.TName)
        self.ax.set_xlabel('Test@Signal Name')
        self.ax.set_ylabel('Value' + unit)
        self.ax.set_xticks(rotation=225)
        self.draw()


class DrawWaveForm_PyChart():
    def __init__(self):
        self.DUT_num_l = None
        self.WF_PD = None
        self.TName = []
        self.xy_dict = None
        self.y_axis = []
        self.unit = None

    def init(self):
        self.WF_PD = glv.WaveForm_pd.copy()
        glv.Html_Path = glv.Current_Path + '\\' + 'html\\'
        data_y = 0
        x_axis_count = 0
        self.DUT_num_l = []
        self.xy_dict = {}
        self.y_axis = []
        self.unit = None
        self.TName = []
        index_cnt = 0
        glv.Chart_Success = False
        for index, row in self.WF_PD.iterrows():
            self.y_axis.append([])
            x_axis_count += 1
            self.TName.append(self.WF_PD.at[index, str(dwf_gs.TestName)] + '@' + self.WF_PD.at[
                index, str(dwf_gs.Signal)])
            self.unit = '(' + self.WF_PD.at[index, str(dwf_gs.Unit)] + ')'
            for dut in range(glv.dut_count):
                data_y += 1
                DUT_num = 'DUT_' + str(glv.DUT_NO[dut])
                self.DUT_num_l.append(DUT_num)
                # self.DUT_V[dut] = self.WF_PD.at[index, DUT_num]
                self.y_axis[index_cnt].append(self.WF_PD.at[index, DUT_num])
            index_cnt += 1
        self.xy_dict = dict(zip(self.TName, self.y_axis))

    def CurveGraph(self):
        box_dict = {'t1_qaz': [1, 2, 3], 't2_wsx': [4, 5, 6]}
        page = Page(layout=Page.DraggablePageLayout)
        scatter = Scatter()
        for key, value in box_dict.items():
            scatter.add_xaxis(key)
            scatter.add_yaxis(key, value)
        scatter.set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况1"))
        page.add(scatter)
        page.render(glv.char_name)
        # os.system(glv.char_name)
        glv.Chart_Success = True

    def LineChart(self):
        line = Line()
        page = Page(layout=Page.DraggablePageLayout)
        glv.char_name = dwf_gts.Chart_Html + '.html'
        line.add_xaxis(self.DUT_num_l[0:glv.dut_count])
        for key, value in self.xy_dict.items():
            line.add_yaxis(key, value)
        line.set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                             axislabel_opts=opts.LabelOpts(rotate=15)
                             )
        page.add(line)
        page.render(glv.char_name)
        # os.system(glv.char_name)
        glv.Chart_Success = True

    def ScatterDiagram(self):
        page = Page(layout=Page.DraggablePageLayout)
        scatter = Scatter()
        glv.char_name = glv.Html_Path + dwf_gts.Chart_Html + '.html'
        if glv.dut_count <= 5:
            rotate_cnt = 0
        else:
            rotate_cnt = 30
        scatter.add_xaxis(glv.DUT_NO)
        for key, value in self.xy_dict.items():
            scatter.add_yaxis(key, value)
        scatter.set_global_opts(title_opts=opts.TitleOpts(title="Test Result"),
                                toolbox_opts=opts.ToolboxOpts(is_show=False,
                                                              orient="vertical",
                                                              feature=opts.ToolBoxFeatureOpts(
                                                                  save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                                                      type_='jpeg',
                                                                      name=self.TName[0]))),
                                xaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                                                         axislabel_opts=opts.LabelOpts(rotate=rotate_cnt)),
                                yaxis_opts=opts.AxisOpts(split_number=10)
                                )
        scatter.set_series_opts(label_opts=opts.LabelOpts(is_show=False)
                                )
        page.add(scatter)
        page.render(glv.char_name)
        # os.system(glv.char_name)
        glv.Chart_Success = True
        if glv.SaveOpt == dwf_gts.none:
            pass
        elif glv.SaveOpt == dwf_gts.Combination:
            save_path = r'C:\007\PythonProject\Ref_Data\10125AE\OutputImage' + '\\' + self.TName[0] + '.png'
            make_snapshot(snapshot, page.render(), save_path)
        elif glv.SaveOpt == dwf_gts.Separation:
            Sub_Pro_1 = multiprocessing.Process(target=ScatterProcess, args=(glv.Html_Path, self.xy_dict, glv.DUT_NO,
                                                rotate_cnt, ))
            Sub_Pro_1.start()

    def Histogram(self):
        pass

    def BoxPlots(self):
        page = Page(layout=Page.DraggablePageLayout)
        box_plot = Boxplot()
        glv.char_name = dwf_gts.Chart_Html + '.html'
        box_plot.add_xaxis([''])
        print(self.y_axis)
        print(self.xy_dict)
        for index in range(len(self.TName)):
            L_TwoD = glv.List_OneD2TwoD(self.y_axis[index], glv.dut_count)
            print(self.TName[index], L_TwoD)
            box_plot.add_yaxis(self.TName[index], box_plot.prepare_data(L_TwoD))

        box_plot.set_global_opts(title_opts=opts.TitleOpts(title="Test Result"),
                                toolbox_opts=opts.ToolboxOpts(is_show=True),
                                xaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_on_zero=False))
                                )
        box_plot.set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                                axislabel_opts=opts.LabelOpts(rotate=15)
                                )
        page.add(box_plot)
        page.render(glv.char_name)
        # os.system(glv.char_name)
        glv.Chart_Success = True


def ScatterProcess(HtmlPath, xy_dict, DUT_num_l, rotate_cnt):
    xy_dict = xy_dict
    DUT_num_l = DUT_num_l
    for key, value in xy_dict.items():
        page = Page(layout=Page.DraggablePageLayout)
        scatter = Scatter()
        scatter.add_xaxis(DUT_num_l[0:len(DUT_num_l)])
        save_name = HtmlPath + key + '.html'
        save_path = r'C:\007\PythonProject\Ref_Data\10125AE\OutputImage' + '\\' + key + '.png'
        scatter.add_yaxis(key, value)
        scatter.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        scatter.set_global_opts(title_opts=opts.TitleOpts(title="Test Result"),
                                xaxis_opts=opts.AxisOpts(
                                                         axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                                                         axislabel_opts=opts.LabelOpts(rotate=rotate_cnt)),
                                yaxis_opts=opts.AxisOpts(split_number=10))
        page.add(scatter)
        page.render(save_name)
        # os.system(save_name)
        make_snapshot(snapshot, page.render(), save_path)

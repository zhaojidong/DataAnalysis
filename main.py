#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: Ansel.Zhao
@file: main.py
@time: 2022/5/23 9:00
"""
import sys, re, linecache, os, time, glovar as glv, TRY
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from DataAnalysis import Ui_MainWindow
import CreatFile, HandleLogFIle
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QWidget, QVBoxLayout, QPushButton, QApplication
import numpy as np

from matplotlib import pyplot as plt
import matplotlib
# matplotlib.use('QtAgg')  # 指定渲染后端。QtAgg后端指用Agg二维图形库在Qt控件上绘图。
# from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar

MF = TRY.MyFigure()
gs = glv.global_str()
gts = glv.global_table_str()
test_name_dict = {}
signal_list = []
log_file_path = r''


class HT_DataAnalysis_UI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):  # parent=None,so the HaiTu_UI is the topmost window
        super(HT_DataAnalysis_UI, self).__init__(
            parent)  # the super().__init__() excutes the constructor fo father, then we can use the property of father
        self.first_pd_rows = None
        self.original_dut_result = None
        self.final_pd = None
        self.yeild = None
        self.tree_item = None
        self.count = None
        self.file_path = None
        self.open_file_path = None
        self.file_total = None
        self.test_item = None
        self.file_name_list = None
        self.root = None
        self.init()
        # self.plotfig()


    def init(self):
        self.setupUi(myWindow)
        myWindow.setWindowTitle('海图微数据分析工具')
        # myWindow.setWindowIcon(QIcon(r'D:\Python\MyLogo\log_snail.jpeg'))
        # self.create_tree()
        self.button_handler()
        # self.initFigure()


    def button_handler(self):
        self.btn_yeild.clicked.connect(lambda: self.handle_checked_item())
        self.actionOpen.triggered.connect(lambda: HT_DataAnalysis_UI.actionOpen(self))

    def actionOpen(self):
        self.handleDisplay('<font color=\"#0000FF\">---- Loading the log file...  ----<font>')
        glv.selected_file_list, fileType = QFileDialog.getOpenFileNames(self, "文件选择", r"C:\007\PythonProject\DataAnalysis", "所有文件 (*);;文本文件 (*.txt)")  # D:\\
        if len(glv.selected_file_list) == 0:
            self.handleDisplay('No object selected!')
            return
        self.tree.clear()
        self.create_tree()

    def create_tree(self):
        tree_pd, final_pd, file_name_list, file_total = HandleLogFIle.ParseLogFile()
        self.handleDisplay(str(len(glv.selected_file_list)) + ' files been selected')
        self.handleDisplay('Dut count = ' + str(glv.dut_count))
        self.final_pd = final_pd
        self.file_name_list = file_name_list
        self.file_total = file_total
        # pd_get = self.handle_logFile()
        self.first_pd_rows = len(tree_pd)
        # set tree's column
        self.tree.setColumnCount(3)
        # set the title
        self.tree.setHeaderLabels(['Key', 'Pass', 'Fail'])
        self.tree.setColumnWidth(0, 250)
        self.tree.setColumnWidth(1, 40)
        self.tree.setColumnWidth(2, 40)
        self.root = QTreeWidgetItem(self.tree)
        self.root.setText(0, 'Test Items')
        self.root.setCheckState(0, Qt.Unchecked)
        loop_count = 0
        while loop_count < (self.first_pd_rows - 1):
            TestName = tree_pd.iloc[loop_count].at[str(gs.TestName)]  # at['TestName']
            if TestName == glv.end_label:
                break
            child1 = QTreeWidgetItem()
            child1.setText(0, TestName)
            self.root.addChild(child1)
            child1.setCheckState(0, Qt.Unchecked)
            while TestName == tree_pd.iloc[loop_count].at[str(gs.TestName)]:
                SignalName = tree_pd.iloc[loop_count].at[str(gs.Signal)]
                child2 = QTreeWidgetItem()
                child2.setText(0, SignalName)
                child2.setText(1, str(tree_pd.iloc[loop_count].at[str(gs.PASS_Count)]))
                child2.setText(2, str(tree_pd.iloc[loop_count].at[str(gs.Fail_Count)]))
                child1.addChild(child2)
                child2.setCheckState(0, Qt.Unchecked)
                loop_count = loop_count + 1
        # 加载根节点的所有属性与子控件
        self.tree.addTopLevelItem(self.root)
        # 节点全部展开
        # self.tree.expandAll()
        # self.setCentralWidget(self.tree)
        self.tree.itemChanged.connect(self.handlechanged)
        self.tree.itemChanged.connect(self.__UpdateParent)
        self.display_endInfo()

    def handlechanged(self, item, column):
        # f_list = ()
        # c_list = ()
        # 获取选中节点的子节点个数
        self.count = item.childCount()
        self.tree_item = item
        check_status = True
        # 如果被选中
        if item.checkState(column) == Qt.Checked:
            # f_list.append(item.text(column))
            # 连同下面子子节点全部设置为选中状态
            for baby in range(self.count):
                # c_list.append(item.child(baby).text(column))
                if item.child(baby).checkState(0) != Qt.Checked:
                    item.child(baby).setCheckState(0, Qt.Checked)

        # 如果取消选中
        elif item.checkState(column) == Qt.Unchecked:
            # 连同下面子子节点全部设置为取消选中状态
            for baby in range(self.count):
                if item.child(baby).checkState != Qt.Unchecked:
                    item.child(baby).setCheckState(0, Qt.Unchecked)

    def __UpdateParent(self, child):
        parent = child.parent()
        if parent is None or parent is self:
            return

        partiallySelected = False
        selectedCount = 0
        childCount = parent.childCount()
        for i in range(childCount):
            childItem = parent.child(i)
            if childItem.checkState(0) == Qt.Checked:
                selectedCount += 1
            elif childItem.checkState(0) == Qt.PartiallyChecked:
                partiallySelected = True

        if partiallySelected:
            parent.setCheckState(0, Qt.PartiallyChecked)
        else:
            if selectedCount == 0:
                parent.setCheckState(0, Qt.Unchecked)
            elif selectedCount > 0 and selectedCount < childCount:
                parent.setCheckState(0, Qt.PartiallyChecked)
            else:
                parent.setCheckState(0, Qt.Checked)
        self.__UpdateParent(parent)

    # traverse the tree, get the checked and unchecked item
    def traverse_tree(self):
        """traverse node"""
        checked_items_dict = {}
        result_check = 3
        item = self.tree.topLevelItem(0)  # get root node
        test_counter = item.childCount()
        all_signal = 0
        c_list = []
        note_checked_count = 0
        for i in range(0, test_counter):
            test_name = item.child(i)
            count = test_name.childCount()  # get the current node count of the son
            if test_name.checkState(0) == Qt.Checked:
                key = item.child(i).text(0)
                result_check = 1
                if count != 0:
                    for j in range(0, count):
                        all_signal = all_signal + 1
                        note_checked_count += 1
                        signal_name = test_name.child(j).text(0)  # the text of son node
                        c_list.append(signal_name)
                checked_items_dict[key] = c_list
            elif test_name.checkState(0) == Qt.PartiallyChecked:    ##########UnChecked
                if count != 0:
                    for j in range(0, count):
                        if test_name.child(j).checkState(0) == Qt.Checked:
                            result_check = 1
                            note_checked_count += 1
                            key = item.child(i).text(0)
                            signal_name = test_name.child(j).text(0)
                            c_list.append(signal_name)
                if c_list:  # do not append to dict if the list is empty
                    checked_items_dict[key] = c_list
        if result_check != 1:
            result_check = 0
        glv.checked_count_from_tree = note_checked_count
        glv.tree_checked = checked_items_dict
        # print('checked_items_dict:', checked_items_dict)
        return checked_items_dict, result_check

    @classmethod
    def get_traverse_tree(cls):
        get_dict, get_result = cls().traverse_tree()
        print(get_dict)
        print(get_result)
        print('get_traverse_tree')
        return get_result

    def handle_checked_item(self):
        self.handleDisplay('<font color=\"#0000FF\">---- Export to excel...... ----<font>')
        self.traverse_tree()
        HandleLogFIle.handle_FinalPd4tree()
        self.handleDisplay('Yield = ' + str(glv.R_yield) + '%')
        self.ploting()
        # self.plotfig()
        self.gen_report()
        self.display_endInfo()

    def ploting(self):
        if self.comboBox_chart.currentText() == str(gts.Curve_chart):
            print(str(gts.Curve_chart))
            self.plotfig()
        elif self.comboBox_chart.currentText() == str(gts.Histogram):
            print(str(gts.Histogram))
        elif self.comboBox_chart.currentText() == str(gts.Normal_distribution):
            print(str(gts.Normal_distribution))
        else:
            print('No Chart')

    def gen_report(self):
        if self.comboBox_report.currentText() == str(gts.Excel_VP):
            CreatFile.CreateExcel_VP_log()
        else:
            print('No Report')

    def initFigure(self):
        # self.fig = plt.figure()  # create figure object
        # self.canvas = FigureCanvas(self.fig)  # create figure canvas
        # self.figtoolbar = NavigationToolbar(self.canvas, self)  # create figure toolbar
        # gb = QGridLayout(self.groupBox)
        # gb.addWidget(self.figtoolbar)  # add the toolbar to UI
        # gb.addWidget(self.canvas)  # add the canvas to UI
        pass


    def plotfig(self):  # 绘制matplot图形
        # ax = self.fig.subplots()
        # t = np.linspace(0, 2 * np.pi, 50)
        # ax.plot(t, np.sin(t))
        # ax.autoscale_view()
        pass

    # display data with textEdit append
    def handleDisplay(self, data):
        self.textEdit.append(data)
        app.processEvents()

    def display_endInfo(self):
        # self.handleDisplay('<font color=\"#0000FF\">---- I AM FREE...... ----<font>')
        self.handleDisplay(str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        self.handleDisplay('------------------------------------------')
        self.handleDisplay('\r\n')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = QMainWindow()
    HTUI = HT_DataAnalysis_UI()
    myWindow.show()
    sys.exit(app.exec_())

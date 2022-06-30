#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: Ansel.Zhao
@file: main.py
@time: 2022/5/23 9:00
"""
import sys, re, linecache, os, time, glovar as glv, TRY
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QUrl
from DataAnalysis import Ui_MainWindow
import CreatFile, HandleLogFIle
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QWidget, QVBoxLayout, QPushButton, QApplication
import numpy as np
import mplcursors
from matplotlib import pyplot as plt
import matplotlib
from DrawWaveForm import DrawWaveForm as DWF, DrawWaveForm_PyChart as DWFPC
import StatisticalAnalysis as SA
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineWidgets import *
matplotlib.use('QtAgg')  # 指定渲染后端。QtAgg后端指用Agg二维图形库在Qt控件上绘图。
# matplotlib.use('Qt5Agg')
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

gs = glv.global_str()
gts = glv.global_table_str()
gi = glv.global_init()
test_name_dict = {}
signal_list = []

class HT_DataAnalysis_UI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):  # parent=None,so the HaiTu_UI is the topmost window
        super(HT_DataAnalysis_UI, self).__init__(
            parent)  # the super().__init__() excutes the constructor fo father, then we can use the property of father
        self.hboxLayout = None
        self.ChartHtml = None
        self.gb = None
        self.figtoolbar = None
        self.canvas = None
        self.error = True
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
        self.hboxLayout = QHBoxLayout(self)
        self.init()

    def init(self):
        self.setupUi(myWindow)
        myWindow.setWindowTitle('海图微数据分析工具')
        self.progressBar.setRange(0, 0)
        glv.Current_Path = os.getcwd()
        # myWindow.setWindowIcon(QIcon(r'D:\Python\MyLogo\log_snail.jpeg'))
        self.init_show()
        self.button_handler()
        self.initChart()

    def init_show(self):
        self.CH = QWebEngineView(self.ChartHtml)
        self.CH.setHtml('''<!DOCTYPE html>
                           <html lang="en">
                           <head>
                               <meta charset="UTF-8">
                               <title>Title</title>
                           </head>
                           <body>
                           <!--<br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />-->
                           <!--<h1>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;海图微电子</h1>-->
                           <!--<h1>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&ensp;DISPLAY CHART</h1>-->
                           <img src="static/123.jpg" alt='image' width="925" height="600">
                           </body>
                           </html>''')
        self.CH.setGeometry(0, 0, 1200, 1000)

    def button_handler(self):
        self.btn_yeild.clicked.connect(lambda: self.handle_checked_item())
        self.actionOpen.triggered.connect(lambda: HT_DataAnalysis_UI.actionOpen(self))
        self.btn_abort.clicked.connect(lambda: self.abortProcess())

    def abortProcess(self):
        try:
            glv.Sub_Process.terminate()  # stop the Process
            message = 'Killed Process ' + str(glv.Process_PPID) + '--Terminate Saving!!!'
            self.handleDisplay('<font color=\"#FF4500\">' + message + '<font>')
            glv.Sub_Process.join()  # Avoid zombie processes
        except OSError:
            print('no process')


    def actionOpen(self):
        self.handleDisplay('<font color=\"#0000FF\">---- Loading the log file...  ----<font>')
        glv.selected_file_list, fileType = QFileDialog.getOpenFileNames(self, "文件选择",
                                                                        r"C:\007\PythonProject\DataAnalysis",
                                                                        "所有文件 (*);;文本文件 (*.txt)")  # D:\\
        if len(glv.selected_file_list) == 0:
            self.handleDisplay('No object selected!')
            self.error = True
            return
        self.error = False
        self.init_glv()
        self.tree.clear()
        self.create_tree()

    def init_glv(self):
        glv.DUT_NO = []

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
        # Get the number of children of the selected node
        self.count = item.childCount()
        self.tree_item = item
        # if check
        if item.checkState(column) == Qt.Checked:
            # All the sub-nodes are set to select
            for baby in range(self.count):
                if item.child(baby).checkState(0) != Qt.Checked:
                    item.child(baby).setCheckState(0, Qt.Checked)

        # if uncheck
        elif item.checkState(column) == Qt.Unchecked:
            # All the sub-nodes are set to deselect
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
            elif 0 < selectedCount < childCount:
                parent.setCheckState(0, Qt.PartiallyChecked)
            else:
                parent.setCheckState(0, Qt.Checked)
        self.__UpdateParent(parent)

    # traverse the tree, get the checked and unchecked item
    def traverse_tree(self):
        """traverse node"""
        checked_items_dict = {}
        result_check = 0
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
            elif test_name.checkState(0) == Qt.PartiallyChecked:
                c_list = []
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
        glv.checked_count_from_tree = note_checked_count
        glv.tree_checked = checked_items_dict
        if result_check:
            self.error = False
        return checked_items_dict, result_check

    @classmethod
    def get_traverse_tree(cls):
        get_dict, get_result = cls().traverse_tree()
        print(get_dict)
        print(get_result)
        print('get_traverse_tree')
        return get_result

    def handle_checked_item(self):
        # self.progressBar.setRange(100)
        self.handleDisplay('<font color=\"#0000FF\">---- Export to excel...... ----<font>')
        if self.error:
            self.handleDisplay('No item was selected!!!')
            self.progressBar.setValue(100)
            return
        checked_dict, checked_res = self.traverse_tree()
        if not checked_res:
            self.handleDisplay('No item was selected!!!')
            self.progressBar.setValue(100)
            return
        HandleLogFIle.handle_FinalPd4tree()
        self.handleDisplay('Yield = ' + str(glv.R_yield) + '%')
        self.ploting()
        self.gen_report()
        self.display_endInfo()

    def gen_report(self):
        if self.comboBox_report.currentText() == str(gts.Excel_VP):
            CreatFile.CreateExcel_VP_log()
        else:
            print('No Report')

    def initFigure(self):
        self.canvas = DWF()
        self.figtoolbar = NavigationToolbar(self.canvas, self)
        self.gb = QGridLayout(self.groupBox)
        self.gb.addWidget(self.figtoolbar)  # add the toolbar to UI
        self.gb.addWidget(self.canvas)  # add the canvas to UI

    # def initPyeCharts(self):
    def initChart(self):
        self.Py_Echart = DWFPC()
        # self.frame = QFrame(self)
        # self.mainhboxLayout
        # self.hboxLayout.addWidget(myWindow)
        # self.CH = QWebEngineView(self.ChartHtml)
        # self.CH.setGeometry(0, 0, 1200, 1000)
        # self.CH.
        # self.hboxLayout.addWidget(self.CH, 0, Qt.AlignVCenter)
        # self.hboxLayout.setSpacing(0)
        # self.setCentralWidget(self.CH)
        # self.CH.page().fullScreenRequested.connect(QWebEngineFullScreenRequest.accept)
        # self.CH.load(QUrl('file:///C:/007/PythonProject/DataAnalysis/Chart_Html.html'))
        # self.CH.setGeometry(0, 0, 1200, 1000)
        # self.gb = QGridLayout(self.groupBox)
        # self.gb.addWidget(self.CH)
        # self.ChartHtml.setHtml('file:///C:/007/PythonProject/DataAnalysis/ScatterDiagram.html')
        # self.ChartHtml.url()
        # self.CH.load(QUrl('file:///C:/007/PythonProject/DataAnalysis/ScatterDiagram.html'))
        # print('file:///C:/007/PythonProject/DataAnalysis/ScatterDiagram.html')
        # self.CH.setContextMenuPolicy(Qt.NoContextMenu)
        # self.CH.setGeometry(0,0,1200,1000)
        # self.CH(self.ChartHtml)
        # self.hboxLayout.addWidget(self.ChartHtml)
        # self.gb = QGridLayout(self.groupBox)
        # # print('3')
        # self.gb.addWidget(self.ChartHtml)
        # self.hl.addWidget()
        # url = 'file:///C:/007/PythonProject/DataAnalysis/' + glv.char_name
        # print('url:', url)
        # 打开本地html文件
        # self.myHtml.load(QUrl(url))
        # self.myHtml.load(QUrl("bar1.html"))   #无法显示，要使用绝对地址定位，在地址前面加上 file:/// ，将地址的 \ 改为/
        # 打开网页url
        # self.myHtml.load(QUrl(url))
        # self.gb = QGridLayout(self.groupBox)
        # self.gb.addWidget(self.myHtml)  # add the toolbar to UI
        # self.hboxLayout.addWidget(self.myHtml)
        # self.setLayout(self.mainhboxLayout)
        # self.browser.load(QUrl(url))

    def ploting(self):
        # self.gb.deleteLater()
        # self.canvas.init()
        self.Py_Echart.init()
        if glv.SaveOpt is not None:
            glv.Chart_Checked = True
        glv.SaveOpt = self.comboBox_SaveOpt.currentText()
        if self.comboBox_chart.currentText() == str(gts.Curve_chart):
            print(str(gts.Curve_chart))
            # self.canvas.CurveGraph()
            self.Py_Echart.CurveGraph()
        elif self.comboBox_chart.currentText() == str(gts.Scatter_diagram):
            print(str(gts.Scatter_diagram))
            # self.canvas.ScatterDiagram()
            self.Py_Echart.ScatterDiagram()
        elif self.comboBox_chart.currentText() == str(gts.Histogram):
            print(str(gts.Histogram))
            # self.canvas.Histogram()
            self.Py_Echart.Histogram()
        elif self.comboBox_chart.currentText() == str(gts.Normal_distribution):
            print(str(gts.Normal_distribution))
        elif self.comboBox_chart.currentText() == str(gts.Line_chart):
            print(str(gts.Line_chart))
            self.Py_Echart.LineChart()
        elif self.comboBox_chart.currentText() == str(gts.Box_plots):
            print(str(gts.Box_plots))
            # self.canvas.BoxPlots()
            self.Py_Echart.BoxPlots()
        else:
            self.handleDisplay('This Chart can not show')
            return
        if glv.Chart_Success:
            url = ('file:///' + glv.char_name).replace('\\', '/')
            self.CH.load(QUrl(url))
            # self.CH.load()
        else:
            self.handleDisplay('This Chart can not show')
        # self.label.setPixmap(self.ChartHtml)
        # self.horizontalLayout.addChildWidget(self.ChartHtml)
        # self.gb = QGridLayout(self.groupBox)
        # print('3')
        # self.gb.addWidget(self.ChartHtml)  # add the toolbar to UI
        # print('4')

    # display data with textEdit append
    def handleDisplay(self, data):
        self.textEdit.append(data)
        app.processEvents()

    def display_endInfo(self):
        self.progressBar.setValue(100)
        # self.handleDisplay('<font color=\"#0000FF\">---- I AM FREE...... ----<font>')
        self.handleDisplay(str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        self.handleDisplay('----------------------------------------')
        self.handleDisplay('\r\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = QMainWindow()
    HTUI = HT_DataAnalysis_UI()
    myWindow.show()
    sys.exit(app.exec_())

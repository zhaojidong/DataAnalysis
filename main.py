import sys, re, linecache, os, time, glovar as glv
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt

import CreatFile
from DataAnalysis import Ui_MainWindow
import HandleLogFIle
# from datahandle import Datahandle
import pandas as pd
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QWidget, QVBoxLayout, QPushButton, QApplication

test_name_dict = {}
signal_list = []
log_file_path = r''
pattern1 = re.compile(r'(TCNT#)\s*[0-9](\s*)(SITE#)(\s*)', re.I)  # find 'TCNT# 0        SITE# 0' as start label
pattern2 = re.compile(r'-------------------', re.I)


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

    def init(self):
        self.setupUi(myWindow)
        myWindow.setWindowTitle('海图微数据分析工具')
        myWindow.setWindowIcon(QIcon(r'D:\Python\MyLogo\log_snail.jpeg'))
        # self.create_tree()
        self.button_handler()

    def button_handler(self):
        self.btn_yeild.clicked.connect(lambda: self.handle_checked_item())
        self.actionOpen.triggered.connect(lambda: HT_DataAnalysis_UI.actionOpen(self))

    def actionOpen(self):
        # self.open_file_path = QFileDialog.getExistingDirectory(None, '选择文件夹', r'')  # D:\\
        glv.selected_file_list, fileType = QFileDialog.getOpenFileNames(self, "文件选择", r"D:\Python\Project\DataAnalysis", "所有文件 (*);;文本文件 (*.txt)")  # D:\\
        print(len(glv.selected_file_list))
        if len(glv.selected_file_list) == 0:
            self.handleDisplay('No object selected!')
            return
        self.handleDisplay(str(glv.selected_file_list))
        self.tree.clear()
        self.create_tree()

    # Read log file, covert to pandas format, return the data
    # def handle_logFile(self):
    #     pd.set_option('display.width', None)
    #     # Follow Code: get all files name and file count
    #     self.file_name_list = os.listdir(self.open_file_path)
    #     self.file_total = len(self.file_name_list)
    #     # Follow Code: open file and handle
    #     for i in range(self.file_total):
    #         self.file_path = self.open_file_path + '\\' + self.file_name_list[i]
    #         # fp = open(self.file_path,'rb')
    #         # Follow Code: get line's total sum
    #         count = -1
    #         for count, line in enumerate(open(self.file_path, 'r')):
    #             pass
    #         count += 1
    #         # Follow Code: read line information
    #         for line_data in range(count):
    #             text = linecache.getline(self.file_path, line_data)
    #             # Follow Code: Find the title's line
    #             if re.search(pattern1, text):
    #                 # after title line, the second line is data
    #                 line_target = line_data + 2
    #                 title = linecache.getline(self.file_path, line_data + 1)
    #                 # Follow Code: Title, convert to list
    #                 title_list = title.split()
    #                 title_len = len(title_list)
    #                 execute_once = True
    #                 self.test_item = count - line_target
    #                 for line_target in range(line_target, count):
    #                     text = linecache.getline(self.file_path, line_target)
    #                     # split according to signal space
    #                     line = re.split(r"[ ]+", text)
    #                     # delete '\n':strip() used for \n and space defaulted
    #                     line = [x.strip() for x in line]
    #                     # merger the unit with the front data
    #                     for index, value in enumerate(line):
    #                         if value == 'nV' or value == 'uV' or value == 'mV' or value == 'V' \
    #                                 or value == 'nA' or value == 'uA' or value == 'mA' or value == 'A':
    #                             line[index - 1] = line[index - 1] + line[index]
    #                             del line[index]
    #                     # list max length, append 'None' to
    #                     for add_none_count in range(title_len - len(line)):
    #                         line.append('None')
    #                     # Follow Code: Add the end label to the pandas dataframe
    #                     line_end = ['-']
    #                     line_end = line_end * title_len
    #                     line_end[0] = '-End of data-'
    #                     if str(line[0]).isdigit():
    #                         if execute_once:
    #                             execute_once = False
    #                             NewList = [[x] for x in line]
    #                             pd_dict = dict(zip(title_list, NewList))
    #                         else:
    #                             line_count = 0
    #                             for key in title_list:
    #                                 pd_dict[key] = pd_dict.get(key, []) + [line[line_count]]
    #                                 line_count = line_count + 1
    #                                 if line_count > len(line) - 1:
    #                                     break
    #                 break
    #         final_pd = pd.DataFrame(pd_dict)
    #         final_pd.loc[len(final_pd)] = line_end
    #         return final_pd
    #         # fp.close()
    #         # break

    # get the data(pandas format), and show the data with tree construct
    def create_tree(self):
        tree_pd, final_pd, file_name_list, file_total = HandleLogFIle.ParseLogFile()
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
        self.root = QTreeWidgetItem(self.tree)
        self.root.setText(0, 'Test Items')
        self.root.setCheckState(0, Qt.Unchecked)
        loop_count = 0
        while loop_count < (self.first_pd_rows - 1):
            TestName = tree_pd.iloc[loop_count].at['TestName']
            if TestName == glv.end_label:
                break
            child1 = QTreeWidgetItem()
            child1.setText(0, TestName)
            self.root.addChild(child1)
            child1.setCheckState(0, Qt.Unchecked)
            while TestName == tree_pd.iloc[loop_count].at['TestName']:
                SignalName = tree_pd.iloc[loop_count].at['Signal']
                loop_count = loop_count + 1
                child2 = QTreeWidgetItem()
                child2.setText(0, SignalName)
                child1.addChild(child2)
                child2.setCheckState(0, Qt.Unchecked)
        # 加载根节点的所有属性与子控件
        self.tree.addTopLevelItem(self.root)
        # 节点全部展开
        # self.tree.expandAll()
        # self.setCentralWidget(self.tree)
        self.tree.itemChanged.connect(self.handlechanged)
        self.tree.itemChanged.connect(self.__UpdateParent)

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
        """遍历节点"""
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
        return checked_items_dict, result_check

    @classmethod
    def get_traverse_tree(cls):
        get_dict, get_result = cls().traverse_tree()
        print(get_dict)
        print(get_result)
        print('get_traverse_tree')
        return get_result


    def handle_checked_item(self):
        self.handleDisplay('<font color=\"#0000FF\">---- I AM WORKING...... ----<font>')
        self.traverse_tree()
        # HandleLogFIle.ParseLogFile()
        HandleLogFIle.handle_FinalPd4tree()
        CreatFile.CreateExcel_VP_log()
        self.textEdit.append('.')
        self.textEdit.append('.')
        self.textEdit.append('.')
        self.handleDisplay('<font color=\"#0000FF\">---- I AM FREE...... ----<font>')
        self.handleDisplay(str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        self.handleDisplay('------------------------------------------')

    # display data with textEdit append
    def handleDisplay(self, data):
        self.textEdit.append(data)
        app.processEvents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = QMainWindow()
    HTUI = HT_DataAnalysis_UI()
    myWindow.show()
    sys.exit(app.exec_())

import sys, re, linecache, os, time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt
from DataAnalysis import Ui_MainWindow
import HandleLogFIle
# from datahandle import Datahandle
import pandas as pd
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QWidget, QVBoxLayout, QPushButton, QApplication

test_name_dict = {}
signal_list = []
log_file_path = r'D:\Python\Project\DataAnalysis\1009LAE0039'
pattern1 = re.compile(r'(TCNT#)\s*[0-9](\s*)(SITE#)(\s*)', re.I)
pattern2 = re.compile(r'-------------------', re.I)

class HT_DataAnalysis_UI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):  # parent=None,so the HaiTu_UI is the topmost window
        super(HT_DataAnalysis_UI, self).__init__(
            parent)  # the super().__init__() excutes the constructor fo father, then we can use the property of father
        self.root = None
        self.init()

    def init(self):
        self.setupUi(myWindow)
        myWindow.setWindowTitle('海图微数据分析工具')
        # self.create_tree()
        self.button_handler()

    def button_handler(self):
        self.btn_yeild.clicked.connect(lambda: self.handle_checked_item())  #
        self.actionOpen.triggered.connect(lambda: HT_DataAnalysis_UI.actionOpen(self))

    def actionOpen(self):
        self.open_file_path = QFileDialog.getExistingDirectory(None,'选择文件夹','D:')
        self.tree.clear()
        self.create_tree()
        print(self.open_file_path)

    # Read log file, covert to pandas format, return the data
    def handle_logFile(self):
        pd.set_option('display.width', None)
        # Follow Code: get all files name and file count
        self.file_name_list = os.listdir(self.open_file_path)
        self.file_total = len(self.file_name_list)
        # Follow Code: open file and handle
        for i in range(self.file_total):
            self.file_path = self.open_file_path + '\\' + self.file_name_list[i]
            fp = open(self.file_path,'rb')
            # Follow Code: get line total sum
            count = -1
            for count, line in enumerate(open(self.file_path, 'r')):
                pass
            count += 1
            # Follow Code: read line information
            for line_data in range(count):
                text = linecache.getline(self.file_path, line_data)
                # Follow Code: Find the title's line
                if re.search(pattern1, text):
                    # after title line, second line  is data
                    line_target = line_data + 2
                    title = linecache.getline(self.file_path, line_data + 1)
                    # Follow Code: Title, convert to list
                    title_list = title.split()
                    title_len = len(title_list)
                    execute_once = True
                    for line_target in range(line_target, count):
                        text = linecache.getline(self.file_path, line_target)
                        # split according to signal space
                        line = re.split(r"[ ]+", text)
                        # delete '\n':strip() used for \n and space defaulted
                        line = [x.strip() for x in line]
                        # merger the unit with before data
                        for index,value in enumerate(line):
                            if value == 'nV' or value == 'uV' or value == 'mV' or value == 'V' \
                               or value == 'nA' or value == 'uA' or value == 'mA' or value == 'A':
                                line[index-1] = line[index-1] + line[index]
                                del line[index]
                        # list max length, append 'None' to
                        for add_none_count in range(title_len-len(line)):
                            line.append('None')
                        # Follow Code: Add the end label to the pandas dataframe
                        line_end = ['-']
                        line_end = line_end * title_len
                        line_end[0] = '-End of data-'
                        if str(line[0]).isdigit():
                            if execute_once:
                                execute_once = False
                                NewList = [[x] for x in line]
                                pd_dict = dict(zip(title_list,NewList))
                            else:
                                line_count = 0
                                for key in title_list:
                                    pd_dict[key] = pd_dict.get(key, []) + [line[line_count]]
                                    line_count = line_count + 1
                                    if line_count > len(line)-1:
                                        break
                    break
            final_pd = pd.DataFrame(pd_dict)
            final_pd.loc[len(final_pd)] = line_end
            return final_pd
            fp.close()
            break

    # get the data(pandas format), and show the data with tree construct
    def create_tree(self):
        pd_get = self.handle_logFile()
        pd_rows = len(pd_get)
        # set tree's column
        self.tree.setColumnCount(2)
        # set the title
        self.tree.setHeaderLabels(['Key', 'Value'])
        self.tree.setColumnWidth(0, 300)
        self.root = QTreeWidgetItem(self.tree)
        self.root.setText(0, 'Test Items')
        self.root.setCheckState(0, Qt.Unchecked)
        loop_count = 0
        while loop_count < (pd_rows - 1):
            TestName = pd_get.iloc[loop_count].at['TestName']
            if TestName == '-End of data-':
                break
            child1 = QTreeWidgetItem()
            child1.setText(0, TestName)
            self.root.addChild(child1)
            child1.setCheckState(0, Qt.Unchecked)
            while (TestName == pd_get.iloc[loop_count].at['TestName']):
                SignalName = pd_get.iloc[loop_count].at['Signal']
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

    def handlechanged(self, item, column):
        # f_list = list()
        # c_list = list()
        # 获取选中节点的子节点个数
        count = item.childCount()
        # 如果被选中
        if item.checkState(column) == Qt.Checked:
            # f_list.append(item.text(column))
            # 连同下面子子节点全部设置为选中状态
            for baby in range(count):
                # c_list.append(item.child(baby).text(column))
                if item.child(baby).checkState(0) != Qt.Checked:
                    item.child(baby).setCheckState(0, Qt.Checked)
        # 如果取消选中
        if item.checkState(column) == Qt.Unchecked:
            # 连同下面子子节点全部设置为取消选中状态
            for baby in range(count):
                if item.child(baby).checkState != Qt.Unchecked:
                    item.child(baby).setCheckState(0, Qt.Unchecked)

    # traverse the tree, get the checked and unchecked item
    def traverse_tree(self):
        """遍历节点"""
        f_dict = {}
        result_check = 0
        item = self.tree.topLevelItem(0)  # get root node
        test_counter = item.childCount()
        for i in range(0, test_counter):
            if item.checkState(0) == Qt.Checked:
                result_check = 1
                break
            elif item.checkState(0) == Qt.Unchecked:
                c_list = list()
                result_check = 2
                test_name = item.child(i)
                if test_name.checkState(0) == Qt.Checked:
                    key = item.child(i).text(0)
                    result_check = 0
                    count = test_name.childCount()  # get the current node count of the son
                    if count != 0:
                        for j in range(0, count):
                            signal_name = test_name.child(j).text(0)  # the text of son node
                            c_list.append(signal_name)
                    f_dict[key] = c_list
                elif test_name.checkState(0) == Qt.Unchecked:
                    result_check = 0
                    count = test_name.childCount()
                    if count != 0:
                        for j in range(0, count):
                            if test_name.child(j).checkState(0) == Qt.Checked:
                                key = item.child(i).text(0)
                                signal_name = test_name.child(j).text(0)
                                c_list.append(signal_name)
                    if c_list:  # do not append to dict if the list is empty
                        f_dict[key] = c_list
        print(f_dict)
        print(result_check)
        return f_dict, result_check

    @classmethod
    def get_traverse_tree(cls):
        get_dict, get_result = cls().traverse_tree()
        print(get_dict)
        print(get_result)
        print('get_traverse_tree')
        return get_result
        pass

    def handle_checked_item(self):
        self.textEdit.append('Start to analysis...')
        fail_dut_count = 0
        target_dict, target_result = self.traverse_tree()
        print('target_result:', target_result)
        for i in range(self.file_total):
            fail_break = False
            self.file_path = self.open_file_path + '\\' + self.file_name_list[i]
            print(self.file_path)
            count = -1
            for count, line in enumerate(open(self.file_path, 'r')):
                pass
            count += 1
            # Follow Code: read line information
            for line_data in range(count):
                text = linecache.getline(self.file_path, line_data)
                # Follow Code: Find the title's line
                if re.search(pattern1, text):
                    line_target = line_data + 2
                    title = linecache.getline(self.file_path, line_data + 1)
                    # Follow Code: Title, convert to list
                    title_list = title.split()
                    title_len = len(title_list)
                    execute_once = True
                    for line_target in range(line_target, count):
                        text = linecache.getline(self.file_path, line_target)
                        # split according to signal space
                        line = re.split(r"[ ]+", text)
                        # delete '\n':strip() used for \n and space defaulted
                        line = [x.strip() for x in line]
                        print(line)
                        # merger the unit with before data
                        for index, value in enumerate(line):
                            if value == 'nV' or value == 'uV' or value == 'mV' or value == 'V' \
                                    or value == 'nA' or value == 'uA' or value == 'mA' or value == 'A':
                                line[index - 1] = line[index - 1] + line[index]
                                del line[index]
                        # list max length, append 'None' to
                        for add_none_count in range(title_len - len(line)):
                            line.append('None')
                        # Follow Code: Add the end label to the pandas dataframe
                        line_end = ['-']
                        line_end = line_end * title_len
                        line_end[0] = '-End of data-'
                        if str(line[0]).isdigit():
                            if execute_once:
                                execute_once = False
                                NewList = [[x] for x in line]
                                pd_dict = dict(zip(title_list, NewList))
                            else:
                                line_count = 0
                                for key in title_list:
                                    pd_dict[key] = pd_dict.get(key, []) + [line[line_count]]
                                    line_count = line_count + 1
                                    if line_count > len(line) - 1:
                                        break
            final_pd = pd.DataFrame(pd_dict)
            final_pd.loc[len(final_pd)] = line_end
            # print(final_pd)
            # print('i:',i)
            if target_result == 1:  # all test item been choosed
                for test_name_count in range(0,len(final_pd)):
                    print('result = 0:', final_pd.iloc[test_name_count].at['Result'])
                    if final_pd.iloc[test_name_count].at['Result'] == 'FAIL':
                        fail_break = True
                        fail_dut_count = fail_dut_count + 1
                        break
                # if fail_break == True:
                #     break
            elif target_result == 0:
                for test_name_count in range(0,len(final_pd)):
                    print('target_result == 1')
                    for key, value in target_dict.items():
                        if str(key) == final_pd.iloc[test_name_count].at['TestName']:
                            if final_pd.iloc[test_name_count].at['Result'] == 'FAIL':
                                fail_break = True
                                fail_dut_count = fail_dut_count + 1
                                break
                    if fail_break == True:
                        break
            elif target_result == 2:  # no test item choosed
                self.textEdit.append('NOTE:<<<<<<---Please choose test item!!!--->>>>>>')
                self.textEdit.append('\r\n')
                print('target_result == 2')
                pass
        self.yeild = 1 - (fail_dut_count / self.file_total)
        print('fail_dut_count:',fail_dut_count)
        print('self.file_total:',self.file_total)
        print(self.yeild)
        self.textEdit.append('Finished!!!')
        self.textEdit.append('The yeild is:')
        self.textEdit.append(str(self.yeild))
        self.textEdit.append(str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
        self.textEdit.append('\r\n')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = QMainWindow()
    HTUI = HT_DataAnalysis_UI()
    myWindow.show()
    sys.exit(app.exec_())









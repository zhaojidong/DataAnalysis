import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt
from DataAnalysis import Ui_MainWindow
import HandleLogFIle
import pandas as pd
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QWidget, QVBoxLayout, QPushButton, QApplication


class HT_DataAnalysis_UI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):  # parent=None,so the HaiTu_UI is the topmost window
        super(HT_DataAnalysis_UI, self).__init__(
            parent)  # the super().__init__() excutes the constructor fo father, then we can use the property of father
        self.init()

    def init(self):
        self.setupUi(myWindow)
        myWindow.setWindowTitle('海图微数据分析工具')
        self.create_tree()
        self.button_handler()

    def button_handler(self):
        self.btn_yeild.clicked.connect(lambda: self.traverse_tree())  # get_checked(self.root)

    def create_tree(self):
        pd_get = HandleLogFIle.LogFile()
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
        self.tree.expandAll()
        # self.setCentralWidget(self.tree)
        self.tree.itemChanged.connect(self.handlechanged)
        # self.tree.itemChanged.connect(self.get_changable)

    def handlechanged(self, item, column):
        f_list = list()
        c_list = list()
        # 获取选中节点的子节点个数
        count = item.childCount()
        # 如果被选中
        if item.checkState(column) == Qt.Checked:
            # print("checked", item, item.text(column),column)
            f_list.append(item.text(column))
            # print('f_list',f_list)
            # 连同下面子子节点全部设置为选中状态
            for baby in range(count):
                # print('baby',item.child(baby).text(column))
                c_list.append(item.child(baby).text(column))
                # print('c_list',c_list)
                if item.child(baby).checkState(0) != Qt.Checked:
                    item.child(baby).setCheckState(0, Qt.Checked)
        # 如果取消选中
        if item.checkState(column) == Qt.Unchecked:
            # print("unchecked", item, item.text(column))
            # 连同下面子子节点全部设置为取消选中状态
            for baby in range(count):
                if item.child(baby).checkState != Qt.Unchecked:
                    item.child(baby).setCheckState(0, Qt.Unchecked)

    def start_convert(self, item):
        print('start_convert')

    def get_checked(self, node: QTreeWidgetItem) -> list:
        """ 得到当前节点选中的所有分支， 返回一个 list """
        temp_list = []
        for item in node.takeChildren():
            # 判断是否选中
            if item.checkState(0) == Qt.Checked:
                temp_list.append(item.text(0))
                # 判断是否还有子分支
                if item.childCount():
                     temp_list.extend(self.get_checked(item))
            node.addChild(item)
        self.tree.expandAll()
        print('get_checked', temp_list)
        return temp_list


    def traverse_tree(self):
        """遍历节点"""
        f_dict = {}
        result_check = 0
        item = self.tree.topLevelItem(0)  # get root node
        test_counter = item.childCount()
        pass
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
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = QMainWindow()
    HTUI = HT_DataAnalysis_UI()
    myWindow.show()
    sys.exit(app.exec_())









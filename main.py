import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt
from DataAnalysis import Ui_MainWindow



class HT_DataAnalysis_UI(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):  # parent=None,so the HaiTu_UI is the topmost window
        super(HT_DataAnalysis_UI, self).__init__(parent)  # the super().__init__() excutes the constructor fo father, then we can use the property of father
        self.init()

    def init(self):
        self.setupUi(myWindow)
        myWindow.setWindowTitle('海图数据分析')
        # 设置列数
        self.tree.setColumnCount(2)
        # 设置树形控件头部的标题
        self.tree.setHeaderLabels(['Key', 'Value'])

        # 设置根节点
        root = QTreeWidgetItem(self.tree)
        root.setText(0, 'Root')
        root.setIcon(0,QIcon('./123.jpg'))

        # todo 优化2 设置根节点的背景颜色
        brush_red = QBrush(Qt.red)
        root.setBackground(0, brush_red)
        brush_blue = QBrush(Qt.blue)
        root.setBackground(1, brush_blue)

        # 设置树形控件的列的宽度
        self.tree.setColumnWidth(0, 150)

        # 设置子节点1
        child1 = QTreeWidgetItem()
        child1.setText(0, 'child1')
        child1.setText(1, 'ios')

        # todo 优化1 设置节点的状态
        child1.setCheckState(0, Qt.Checked)

        root.addChild(child1)

        # 设置子节点2
        child2 = QTreeWidgetItem(root)
        child2.setText(0, 'child2')
        child2.setText(1, '')

        # 设置子节点3
        child3 = QTreeWidgetItem(child2)
        child3.setText(0, 'child3')
        child3.setText(1, 'android')

        # 加载根节点的所有属性与子控件
        self.tree.addTopLevelItem(root)

        # 节点全部展开
        self.tree.expandAll()
        # self.setCentralWidget(self.tree)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = QMainWindow()
    HTUI = HT_DataAnalysis_UI()
    myWindow.show()
    # HTUI.show()
    sys.exit(app.exec_())


from matplotlib import pyplot as plt
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(MyFigure, self).__init__(self.fig) #此句必不可少，否则不能显示图形
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)
    #第四步：就是画图，【可以在此类中画，也可以在其它类中画】
    def plotsin(self):
        self.axes0 = self.fig.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.axes0.plot(t, s)
        self.fig.suptitle("sin")
    def plotcos(self):
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.axes.plot(t, s)
        self.fig.suptitle("cos")

def ppp():
    t = np.arange(0.0, 3.0, 0.01)
    s = np.sin(2 * np.pi * t)
    plt.plot(t, s, color='mediumseagreen', label='GB_ave', marker='d')
    plt.show()


import sys
import numpy as np
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("matplotlib embeded in Python Qt with figure toolbar")
        self.initUI()
        self.plotfig()

    def initUI(self):
        self.fig = plt.figure()  # 创建figure对象
        self.canvas = FigureCanvas(self.fig)  # 创建figure画布
        self.figtoolbar = NavigationToolbar(self.canvas, self)  # 创建figure工具栏

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.canvas)  # 画布添加到窗口布局中
        vlayout.addWidget(self.figtoolbar)  # 工具栏添加到窗口布局中
        self.setLayout(vlayout)

    def plotfig(self):  # 绘制matplot图形
        ax = self.fig.subplots()
        t = np.linspace(0, 2 * np.pi, 50)
        ax.plot(t, np.sin(t))
        ax.autoscale_view()



if __name__ == '__main__':
    # t = np.arange(0.0, 3.0, 0.01)
    # s = np.sin(2 * np.pi * t)
    # plt.plot(t, s, color='mediumseagreen', label='GB_ave', marker='d')
    # plt.show()
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec())
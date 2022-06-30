# # coding='utf-8'
#
# from PyQt5.QtWidgets import QApplication, QWidget,\
#     QProgressBar, QPushButton
# from PyQt5.QtCore import QBasicTimer
# import sys
#
#
# class Gui(QWidget):
#     def __init__(self):
#         super(Gui, self).__init__()
#         self.start()
#
#     def start(self):
#         # 创建父组件是QWidget(主窗体)的进度条
#         self.progress_bar = QProgressBar(self)
#         self.progress_bar.setGeometry(30, 40, 100, 25)
#
#         # 创建内容是'开始',父组件是QWidget的按钮
#         self.button = QPushButton('开始', self)
#         # 将信号clicked与槽self.do相连
#         self.button.clicked.connect(self.do)
#         self.button.move(40, 80)
#
#         # 创建计时器
#         # 计时器的构造函数:
#         """
#             QBasicTimer()
#             QBasicTimer(QBasicTimer)
#         """
#         self.timer = QBasicTimer()
#         # 计时器的初始值设为0
#         self.step = 0
#
#         self.setGeometry(300, 300, 280, 170)
#         self.setWindowTitle('进度条')
#         self.show()
#
#     def do(self):
#         # 判断进度条是否完成,完成则关闭窗体
#         if self.button.text() == '完成':
#             self.close()
#         # 判断计数器是否处于计数状态(没停止)
#         if self.timer.isActive():
#             # 停止计数
#             self.timer.stop()
#             self.button.setText('开始')
#         else:
#             # 如果按了按钮后发现计数器是停止状态\
#             #  (刚开始的状态就是停止状态)的: 就让计数器继续计数
#             # timer.start的两个参数:\
#                 # 第一个:timeout表示计数器最高阈值是100
#                 # 第二个:QObject表示是哪个对象会接受这个timer事件
#             self.timer.start(100, self)
#             self.button.setText('停止')
#
#     # 这个是重写QWidget的方法,这个方法会一直触发
#     def timerEvent(self, e) -> None:
#         # 如果计时器的数值达到了100,就认为进度条满了,\
#         #   因为进度条默认值是0-99
#         if self.step >= 100:
#             # 让计时器停下来
#             self.timer.stop()
#             # 进度条完成后给按钮设置为'完成'
#             self.button.setText('完成')
#             return
#         # 如果计时器的还在计数
#         self.step += 1
#         # 就把计数器增加后的值设置成进度条的值,然后进度条就会动了,\
#         #             注意这里进度条用的值是默认的0-->99
#         self.progress_bar.setValue(self.step)
#
#
# app = QApplication(sys.argv)
# gui = Gui()
# sys.exit(app.exec_())

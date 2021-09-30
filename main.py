# import matplotlib
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import numpy as np
import sys
from GUI.mainWindow import Ui_MainWindow
from drawCurves.DrawCurves import *
from Data.processExcel import *



class MyWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

class CanvasWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

    def contextMenuEvent(self, event) -> None:
        self.menu = QMenu()
        self.editPos = QAction("编辑坐标")
        self.newFigure = QAction("新建")
        self.cancel = QAction("取消")
        self.menu.addAction(self.editPos)
        self.menu.addAction(self.newFigure)
        self.menu.addAction(self.cancel)
        self.menu.exec_(event.globalPos())


class Ui_MyWindow(Ui_MainWindow):
    def __init__(self, mainWindow, canvas):
        self.window = mainWindow
        self.canvas = canvas
        self.setupUi(self.window)

    def setupUi(self, Window):
        super(Ui_MyWindow, self).setupUi(Window)
        self.activateMenu()
        self.main_tabWidget = QTabWidget()
        self.horizontalLayout.addWidget(self.main_tabWidget)

        self.window.setMouseTracking(True)
        self.centralwidget.setMouseTracking(True)

        self.main_tabWidget.setMouseTracking(True)
        self.canvasWidget = CanvasWidget()
        self.canvasLayout = QHBoxLayout()
        self.canvasLayout.addWidget(self.canvas)
        self.canvasWidget.setLayout(self.canvasLayout)
        self.main_tabWidget.addTab(self.canvasWidget, "1")

        self.canvasWidget.setMouseTracking(True)

        self.draw()
        # 几个QWidgets
        # self.button_draw = QPushButton("绘图")
        # 连接事件
        # self.button_draw.clicked.connect(self.draw)
        # self.horizontalLayout.addWidget(self.button_draw)


    def getFunc(self, func, *args, **kwargs):
        self.myFunc = func
        self.dictArgs = kwargs
        self.tupleArgs = args

    def setCanvas(self):
        self.canvas.mpl_connect("motion_notify_event", self.changeMessage)  # 支持鼠标移动

    def draw(self):
        self.setCanvas()
        # 设置布局
        self.canvas.draw()

    # 改变状态栏信息
    def changeMessage(self, event):
        # message = str(event.x-21) + "," + str(event.y-21)
        message = str(event.xdata) + "," + str(event.ydata)
        self.statusbar.showMessage(message)

    def activateMenu(self):
        data = processData()
        print("yes")
        self.action.triggered.connect(lambda: data.saveData())
        self.action_2.triggered.connect(lambda: data.importData())

















# 运行程序
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MyWindow()
    draw_lines = DrawLines()
    canvas = draw_lines.getCanvas()
    ui_window = Ui_MyWindow(main_window, canvas)
    main_window.show()
    app.exec()




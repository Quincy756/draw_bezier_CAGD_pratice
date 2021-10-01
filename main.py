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
from PyQt5.QtCore import Qt
import math


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
    def __init__(self, mainWindow):

        self.draw_lines = DrawLines()
        self.canvas = self.draw_lines.getCanvas()

        self.window = mainWindow
        self.setupUi(self.window)

    def setupUi(self, Window):
        super(Ui_MyWindow, self).setupUi(Window)
        self.data = None
        self.x, self.y = [1, 2, 6, 20, 30], [2, 20, 32, 35, 40]

        self.keyPressFlag = False
        self.dragPicFlag = False
        self.currentIndex = 0

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
        self.canvas.mpl_connect("button_press_event", self.keyPress)  # 支持鼠标移动
        self.canvas.mpl_connect("button_release_event", self.keyRelease)  # 支持鼠标移动

    def draw(self):
        self.setCanvas()
        self.draw_lines.draw(self.x, self.y)
        # 设置布局
        self.canvas.draw()
        self.exportDataToTable([self.x, self.y])

    # 改变状态栏信息
    def changeMessage(self, event):
        # message = str(event.x-21) + "," + str(event.y-21)
        x_select, y_select = event.xdata, event.ydata
        message = ""
        if self.dragPicFlag:
            self.x[self.currentIndex], self.y[self.currentIndex] = round(x_select, 1), round(y_select, 1)
            self.draw_lines.draw(self.x, self.y)
        else:
            try:
                index = 0
                for x, y in zip(self.draw_lines.x, self.draw_lines.y):
                    if self.getPointDistance((x, y), (x_select, y_select)) < 0.5:
                        message = str(x) + "," + str(y)
                        self.main_tabWidget.setCursor(Qt.SizeAllCursor)
                        if self.keyPressFlag:
                            self.dragPicFlag = True
                            self.currentIndex = index
                            # 替换该点, 取点的三位小数显示到表格中
                            # self.x[self.currentIndex], self.y[self.currentIndex] = round(x_select, 3), round(y_select, 3)
                            # self.draw_lines.draw(self.x, self.y)
                            # self.dragPicFlag = False
                        else:
                            self.dragPicFlag = False
                        break
                    else:
                        if self.dragPicFlag: self.main_tabWidget.setCursor(Qt.SizeAllCursor)
                        else: self.main_tabWidget.setCursor(Qt.ArrowCursor)
                        message = str(x_select) + "," + str(y_select)
                    index += 1
                self.statusbar.showMessage(message)
            except Exception as ex:
                print(ex)

    def keyPress(self, event):
        self.keyPressFlag = True

    def keyRelease(self, event):
        self.keyPressFlag = False
        self.dragPicFlag = False
        self.exportDataToTable([self.x, self.y])
        # 如果点被拖拽
        # if self.dragPicFlag:
            # x, y = event.xdata, event.ydata
            # 替换该点, 取点的三位小数显示到表格中
            # self.x[self.currentIndex], self.y[self.currentIndex] = round(x, 3), round(y, 3)
            # self.draw_lines.draw(self.x, self.y)
            # self.dragPicFlag = False
            # 更新表格
            # self.exportDataToTable([self.x, self.y])

    def getPointDistance(self, p1, p2):
        dis = 0
        for i in range(len(p1)):
            dis += (p1[i]-p2[i])**2
        return dis**0.5



    def activateMenu(self):
        self.process_data = processData(self.data)
        self.action.triggered.connect(lambda: self.process_data.saveData())
        self.action_2.triggered.connect(lambda: self.process_data.exportData())
        self.process_data.getUpdateFunc([self.exportDataToTable, self.getTableData])
        self.setFig()

    def exportDataToTable(self, data=[]):
        rows, cols = len(data[0]), len(data)
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(rows)
        for row in range(rows):
            for col in range(cols):
                item = QTableWidgetItem()
                item.setText(str(data[col][row]))
                self.tableWidget.setItem(row, col, item)

    def getTableData(self):
        data = []
        rows, cols = self.tableWidget.rowCount(), self.tableWidget.columnCount()
        print(rows, cols)
        for col in range(cols):
            temp = []
            for row in range(rows):
                data = self.tableWidget.item(row, col).text()
                print(data)
                if data:
                    temp.append(int(data))
            data.append(temp)
        print(data)
        self.data = data
        self.process_data.setData(self.data)

    def setFig(self):
        self.process_data.setFig(self.draw_lines.getFigure())


# 运行程序
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MyWindow()
    ui_window = Ui_MyWindow(main_window)
    main_window.show()
    app.exec()




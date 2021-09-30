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
    def __init__(self, mainWindow):

        self.draw_lines = DrawLines()
        self.canvas = self.draw_lines.getCanvas()

        self.window = mainWindow
        self.setupUi(self.window)

    def setupUi(self, Window):
        super(Ui_MyWindow, self).setupUi(Window)
        self.data = None
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
        x, y = event.xdata, event.ydata
        message = str(x) + "," + str(y)
        self.statusbar.showMessage(message)









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




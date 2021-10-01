# import matplotlib
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import numpy as np
import sys
from GUI.mainWindow import Ui_MainWindow
from drawCurves.DrawCurves import *
from Data.processExcel import *
from PyQt5.QtCore import Qt
import math
import time
import src

def getIcon(path):
    file_pixmap = QPixmap(path)
    file_fit_pixmap = file_pixmap.scaled(16, 16, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    # 注意 scaled() 返回一个 QPixmap
    return QIcon(file_fit_pixmap)



class MyWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

class CanvasWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

    # 设置右键要执行的函数
    def setContextMenuFunc(self, func):
        self.contextMenuFunc = func

    def contextMenuEvent(self, event) -> None:
        self.contextMenuFunc(event.globalPos())


class InputPointWdt(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.resize(160, 20)
        # 设置窗口为模态
        self.setWindowModality(Qt.ApplicationModal)
        # 设置窗口透明度
        self.setWindowOpacity(0.8)
        self.setWindowFlags(Qt.ToolTip)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.xLineEdit = QLineEdit()
        self.layout.addWidget(self.xLineEdit)
        # 添加分割线
        self.splitter = QLabel("|")
        self.layout.addWidget(self.splitter)
        self.yLineEdit = QLineEdit()
        self.layout.addWidget(self.yLineEdit)
        self.splitter.setMaximumWidth(5)
        self.xLineEdit.setMaximumHeight(25)
        self.yLineEdit.setMaximumHeight(25)


        self.okBtn = QPushButton()
        self.cancelBtn = QPushButton()
        self.okBtn.setMaximumWidth(20)
        self.cancelBtn.setMaximumWidth(20)

        self.okBtn.setFlat(True)
        self.cancelBtn.setFlat(True)
        self.okBtn.setIcon(getIcon(":/resources//MyIcon//check.svg"))
        self.cancelBtn.setIcon(getIcon(":/resources//MyIcon//times.svg"))

        self.layout.addWidget(self.okBtn)
        self.layout.addWidget(self.cancelBtn)
        self.cancelBtn.clicked.connect(lambda: self.close())

    def setLineEditText(self, x, y):
        self.xLineEdit.setText(str(x))
        self.yLineEdit.setText(str(y))
        self.xLineEdit.selectAll()
        self.yLineEdit.selectAll()

    def setCloseFunc(self, func):
        self.closeFunc = func

    def getData(self):
        res = [None]*2
        try:
            res[0], res[1] = float(self.xLineEdit.text()), float(self.yLineEdit.text())
            return res
        except Exception as ex:
            print(ex)
            warning_box = QMessageBox(QMessageBox.Warning, "警告","输入非小数")
            warning_box.exec_()


    def closeEvent(self, a0: QCloseEvent) -> None:
        self.closeFunc()



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
        # 记录鼠标在状态栏中的位置
        self.pos_x, self.pos_y =  0, 0
        self.selectedPoint = ()

        self.keyPressFlag = False
        self.dragPicFlag = False
        self.showPosFlag = False
        self.selectedFlag = False
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
        self.canvasWidget.setContextMenuFunc(self.showContextMenu)

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

    # 双击时创建可以输入位置坐标的，此处x, y 是相对于窗口坐标，不是具体坐标轴中的坐标
    def showPosInput(self):
        if not self.showPosFlag:
            flag = False
            if self.selectedFlag:
                texts = [str(self.selectedPoint[0]), str(self.selectedPoint[1])]
                flag = True
            else:
                texts = [round(self.pos_x, 3), round(self.pos_y, 3)]
                flag = False
            x, y = (QCursor.pos().x(), QCursor.pos().y())
            self.posWidget = InputPointWdt()
            self.posWidget.move(x-120, y-20)
            self.posWidget.setLineEditText(*texts)
            self.posWidget.show()
            self.showPosFlag = True
            self.dragPicFlag = False
            self.posWidget.setCloseFunc(self.closePosInput)
            self.posWidget.okBtn.clicked.connect(lambda: self.updatePointPos(flag))

    # 移动鼠标时改变状态栏信息，拖拽曲线
    def changeMessage(self, event):
        # message = str(event.x-21) + "," + str(event.y-21)
        s = time.time()
        self.pos_x, self.pos_y = event.xdata, event.ydata
        message = ""

        if self.dragPicFlag:
            self.x[self.currentIndex], self.y[self.currentIndex] = round(self.pos_x, 1), round(self.pos_y, 1)
            self.draw_lines.draw(self.x, self.y)
        else:
            try:
                index = 0
                for x, y in zip(self.draw_lines.x, self.draw_lines.y):
                    if self.getPointDistance((x, y), (self.pos_x, self.pos_y)) < 0.5:
                        # 选中
                        self.selectedFlag = True
                        # print(self.selectedFlag)
                        message = str(x) + "," + str(y)
                        self.main_tabWidget.setCursor(Qt.CrossCursor)

                        self.selectedPoint = (x, y)
                        self.currentIndex = index
                        # self.showPosInput()

                        if self.keyPressFlag:
                            self.dragPicFlag = True
                        else:
                            self.dragPicFlag = False
                        break
                    else:
                        # 未选中点时
                        self.selectedFlag = False
                        # self.closePosInput()

                        if self.dragPicFlag: self.main_tabWidget.setCursor(Qt.CrossCursor)
                        else: self.main_tabWidget.setCursor(Qt.ArrowCursor)
                        message = str(round(self.pos_x, 3)) + "," + str(round(self.pos_y, 3))
                    index += 1
                self.statusbar.showMessage(message)
            except Exception as ex:
                pass
                print(ex)

    # 展示右键菜单
    def showContextMenu(self, pos):
        self.menu = QMenu()
        self.editPos = QAction("编辑坐标")
        self.newPoint = QAction("新建")
        self.cancel = QAction("取消")
        self.delete = QAction("删除")
        self.menu.addAction(self.editPos)
        self.menu.addAction(self.newPoint)
        self.menu.addAction(self.delete)
        self.menu.addSeparator()
        self.menu.addAction(self.cancel)
        self.editPos.triggered.connect(self.showPosInput)
        self.newPoint.triggered.connect(self.showPosInput)
        self.delete.triggered.connect(self.deletePoint)

        self.editPos.setEnabled(self.selectedFlag)
        self.delete.setEnabled(self.selectedFlag)

        self.menu.exec_(pos)

    def closePosInput(self):
        if self.showPosFlag:
            self.showPosFlag = False
            self.dragPicFlag = False

    # 改变点或者新增点, flag为True表示编辑点，flag为False表示增加点
    def updatePointPos(self, flag):
        data = self.posWidget.getData()
        self.posWidget.close()
        if data:
            if flag:
                # 替换点坐标
                self.x[self.currentIndex], self.y[self.currentIndex] = data
                self.updateTable(0, data=data, index=self.currentIndex)
            else:
                self.x.append(data[0])
                self.y.append(data[1])
                self.updateTable(1, data)
            self.draw_lines.draw(self.x, self.y)


    # 删除点
    def deletePoint(self):
        if self.selectedFlag:
            self.x.pop(self.currentIndex)
            self.y.pop(self.currentIndex)
            self.draw_lines.draw(self.x, self.y)
            self.updateTable(-1)



    def keyPress(self, event):
        self.keyPressFlag = True

    def keyRelease(self, event):
        self.keyPressFlag = False
        self.dragPicFlag = False
        self.exportDataToTable([self.x, self.y])

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
        self.tableWidget.setColumnCount(cols)
        for row in range(rows):
            for col in range(cols):
                item = QTableWidgetItem()
                item.setText(str(data[col][row]))
                self.tableWidget.setItem(row, col, item)

    def getTableData(self):
        data_list = []
        rows, cols = self.tableWidget.rowCount(), self.tableWidget.columnCount()
        print(rows, cols)
        for col in range(cols):
            temp = []
            for row in range(rows):
                data = self.tableWidget.item(row, col).text()
                print(col, row, data)
                if data:
                    temp.append(int(data))
            data_list.append(temp)
        print(data_list)
        self.data = data_list
        self.process_data.setData(self.data)

    def setFig(self):
        self.process_data.setFig(self.draw_lines.getFigure())

    # 坐标换算， 把绘图框中的坐标和鼠标相对于主窗口的坐标进行换算
    def posConversion(self):
        pass

    # flag: 0修改， 1， 增加， -1， 删除
    def updateTable(self, flag, data=None, index=None):
        print("--------------update Table-----------------")
        if flag == 0:
            x, y = data
            self.tableWidget.item(index, 0).setText(str(x))
            self.tableWidget.item(index, 1).setText(str(y))

        elif flag == 1:
            x, y = data
            rows, cols = self.tableWidget.rowCount(), self.tableWidget.columnCount()
            self.tableWidget.setRowCount(rows+1)
            x_item = QTableWidgetItem()
            y_item = QTableWidgetItem()
            x_item.setText(str(x))
            y_item.setText(str(y))
            self.tableWidget.setItem(rows, 0, x_item)
            self.tableWidget.setItem(rows, 1, y_item)

        else:
            self.tableWidget.removeRow(self.tableWidget.rowCount())




# 运行程序
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyWindow()
    ui_window = Ui_MyWindow(main_window)
    main_window.show()
    app.exec()




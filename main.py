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
from PyQt5.QtCore import Qt, QPoint
import math
import time
import src

def getIcon(path):
    file_pixmap = QPixmap(path)
    file_fit_pixmap = file_pixmap.scaled(16, 16, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    # 注意 scaled() 返回一个 QPixmap
    return QIcon(file_fit_pixmap)

class MyMenu(QMenu):
    def __init__(self):
        super(QMenu, self).__init__()
        self.newPoint = QAction("增加点")
        self.delete = QAction("删除点")
        self.cancel = QAction("取消")
        self.addAction(self.newPoint)
        self.addAction(self.delete)
        self.addSeparator()
        self.addAction(self.cancel)
        self.cancel.triggered.connect(self.close)


class MyPointMenu(QMenu):
    def __init__(self):
        super(QMenu, self).__init__()

class MyTableMenu(QMenu):
    def __init__(self):
        super(QMenu, self).__init__()


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
        self.dataLength = len(self.x)

        self.keyPressFlag = False
        self.dragPicFlag = False
        self.showPosFlag = False
        self.selectedFlag = False
        self.currentIndex = 0
        # 点是否被选中的列表
        self.selectedFlagList = [False]*self.dataLength

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
        self.main_tabWidget.addTab(self.canvasWidget, "tab1")
        self.main_tabWidget.setTabsClosable(True)
        self.main_tabWidget.tabCloseRequested.connect(self.closeCurrentTab)

        self.canvasWidget.setMouseTracking(True)
        self.canvasWidget.setContextMenuFunc(self.showContextMenu)

        # 设置表格行列宽度
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # 设置events_table的右键菜单
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.showTableMenu)

        self.tableWidget.cellDoubleClicked.connect(self.setCurrentItem)
        self.tableWidget.cellChanged.connect(self.checkTableInput)

        self.dockWidget.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.draw()

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
        self.pos_x, self.pos_y = event.xdata, event.ydata
        # 如果鼠标在画图区域内
        if self.pos_x and self.pos_y:
            message = ""
            # 如果按钮按下且处于拖拽状态，直接画出线段
            if self.keyPressFlag and self.dragPicFlag:
                self.x[self.currentIndex], self.y[self.currentIndex] = round(self.pos_x, 1), round(self.pos_y, 1)
                self.draw_lines.draw(self.x, self.y)
            else:
                # 如果已停止拖拽，鼠标移到点集附近时自动选中该点
                index = 0
                for x, y in zip(self.draw_lines.x, self.draw_lines.y):
                    if self.getPointDistance((x, y), (self.pos_x, self.pos_y)) < 0.5:
                        # 选中
                        self.selectedFlag = True
                        # print(self.selectedFlag)
                        message = "已选中 " + "x :" + str(x) + ", y :" + str(y)
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
                        message = "x :" + str(round(self.pos_x, 3)) + ", y :" + str(round(self.pos_y, 3))
                    index += 1
                self.statusbar.showMessage(message)

            if event.dblclick:
                self.doubleClickFlag = True

        # 未移动到绘图区域时时
        else:
            self.statusbar.showMessage("未选中点！")

    # 展示右键菜单
    def showContextMenu(self, pos):
        self.point_menu = MyMenu()
        self.point_menu.editPos = QAction("编辑")
        self.point_menu.insertAction(self.point_menu.newPoint, self.point_menu.editPos)
        self.point_menu.editPos.triggered.connect(self.showPosInput)
        self.point_menu.newPoint.triggered.connect(self.showPosInput)
        self.point_menu.delete.triggered.connect(self.deletePoint)
        self.point_menu.editPos.setEnabled(self.selectedFlag)
        # 如果没有选中点则删除不可用
        if True in self.selectedFlagList:
            self.point_menu.delete.setEnabled(True)
        else:
            self.point_menu.delete.setEnabled(False)

        self.point_menu.exec_(pos)

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
                index = self.currentIndex+1 if True in self.selectedFlagList else self.dataLength
                self.x.insert(index, data[0])
                self.y.insert(index, data[1])
                self.updateTable(1, index=index, data=data)
                self.dataLength += 1
                # print(self.selectedFlagList)
            self.selectedFlagList = [False] * (self.dataLength)
            self.draw_lines.draw(self.x, self.y)

    # 提醒保存
    def closeCurrentTab(self):
        response_btn =  QMessageBox.warning(self.window, "保存提示", "是否保存？", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        if response_btn == QMessageBox.Yes:
            self.process_data.saveData()
        self.main_tabWidget.removeTab(self.main_tabWidget.currentIndex())
        self.tabWidget_2.removeTab(self.tabWidget_2.currentIndex())
    # 删除点
    def deletePoint(self):
        # print("----------------------删除点集------------------------------")
        # print(self.selectedFlagList)
        index_list = [index for index in range(self.dataLength) if self.selectedFlagList[index]]
        self.x = [self.x[index] for index in range(self.dataLength) if index not in index_list]
        self.y = [self.y[index] for index in range(self.dataLength) if index not in index_list]
        # print(self.x, self.y)
        self.selectedFlagList = [self.selectedFlagList[index] for index in range(self.dataLength) if index not in index_list]
        # print(self.selectedFlagList)
        self.draw_lines.draw(self.x, self.y)
        # print(index_list)
        self.updateTable(-1, None, None, index_list)
        self.dataLength = len(self.x)

    def keyPress(self, event):
        # 如果是左键按下
        if event.button == 1:
            # 不是双击左键
            if not event.dblclick:
                self.keyPressFlag = True
                if self.selectedFlag:
                    self.selectedFlagList[self.currentIndex] = not self.selectedFlagList[self.currentIndex]
                else:
                    self.selectedFlagList[self.currentIndex] = False
                print(self.selectedFlagList)
                self.updatePointColor()

    def setCurrentItem(self, row, col):
        self.currentItemText = self.tableWidget.item(row, col).text()

    def checkTableInput(self, row, col):
        try:
            temp = float(self.tableWidget.item(row, col).text())
        except Exception as ex:
            response_btn = QMessageBox.warning(self.tableWidget, "输入错误", "请输入一个小数！", QMessageBox.Yes)
            self.tableWidget.item(row, col).setText(self.currentItemText)

    def updatePointColor(self):
        self.draw_lines.updateScatter(self.selectedFlagList)
        self.canvas.draw()

    def keyRelease(self, event):
        # print(event)
        if not event.dblclick:
            self.keyPressFlag = False
            if self.dragPicFlag:
                self.exportDataToTable([self.x, self.y])
                self.dragPicFlag = False
            elif self.selectedFlag:
                pass

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
        self.statusbar.showMessage("表格数据导入中")
        rows, cols = len(data[0]), len(data)
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(cols)
        for row in range(rows):
            for col in range(cols):
                item = QTableWidgetItem()
                item.setText(str(data[col][row]))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(row, col, item)
        self.statusbar.showMessage("表格数据导入完成！")

    def getTableData(self):
        # print("---------------正在保存信息-------------------")
        data_list = []
        rows, cols = self.tableWidget.rowCount(), self.tableWidget.columnCount()
        for col in range(cols):
            temp = []
            for row in range(rows):
                data = self.tableWidget.item(row, col).text()
                # print(col, row, data)
                if data:
                    temp.append(float(data))
            data_list.append(temp)
        self.data = data_list
        self.process_data.setData(self.data)
        self.statusbar.showMessage("保存完成！")

    def setFig(self):
        self.process_data.setFig(self.draw_lines.getFigure())

    # flag: 0修改， 1， 增加， -1， 删除
    def updateTable(self, flag, data=[0]*2, index=None, rows=[]):
        # print("--------------update Table-----------------")
        index = self.dataLength - 1 if not index else index
        if flag == 0:
            x, y = data
            self.tableWidget.item(index, 0).setText(str(x))
            self.tableWidget.item(index, 1).setText(str(y))

        elif flag == 1:
            x, y = data
            rows, cols = self.tableWidget.rowCount(), self.tableWidget.columnCount()
            self.tableWidget.insertRow(index)
            x_item = QTableWidgetItem()
            y_item = QTableWidgetItem()
            x_item.setTextAlignment(Qt.AlignCenter)
            y_item.setTextAlignment(Qt.AlignCenter)
            x_item.setText(str(x))
            y_item.setText(str(y))
            self.tableWidget.setItem(index, 0, x_item)
            self.tableWidget.setItem(index, 1, y_item)

        else:
            # 逆序删除，防止报错
            rows.reverse()
            for i in rows:
                self.tableWidget.removeRow(i)
        self.statusbar.showMessage("表格数据更新完成！")

    def showTableMenu(self):
        self.table_menu = MyMenu()
        if self.tableWidget.selectedItems():
            self.table_menu.delete.setEnabled(True)
        else:
            self.table_menu.delete.setEnabled(False)

        self.table_menu.delete.triggered.connect(lambda: self.changeTableData(False))
        self.table_menu.newPoint.triggered.connect(lambda: self.changeTableData(True))

        self.table_menu.exec_(QCursor.pos())

    def changeTableData(self, flag):
        index = set()
        if not self.tableWidget.selectedItems():
            index.add(self.tableWidget.rowCount() - 1)
        else:
            for item in self.tableWidget.selectedItems():
                index.add(item.row())
        index = list(index)
        if flag:
            self.updateTable(1, data=[0, 0], index=index[0]+1, rows=list(index))
        else:
            self.updateTable(-1, rows=list(index))



# 运行程序
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyWindow()
    ui_window = Ui_MyWindow(main_window)
    main_window.show()
    app.exec()




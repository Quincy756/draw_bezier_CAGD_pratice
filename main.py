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
from PyQt5.QtCore import pyqtSignal
import math
import time
import src

def getIcon(path):
    file_pixmap = QPixmap(path)
    file_fit_pixmap = file_pixmap.scaled(16, 16, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    # 注意 scaled() 返回一个 QPixmap
    return QIcon(file_fit_pixmap)


class MyTab():
    def __init__(self):
        # self.data = [[1, 2, 6, 20, 30], [2, 20, 32, 35, 40]]
        self.data = [[0], [0]]
        self.draw_lines = DrawLines()
        self.canvas = self.draw_lines.getCanvas()

        # 记录鼠标在画布中的位置
        self.pos_x, self.pos_y = 0, 0
        self.selectedPoint = ()
        self.dataLength = len(self.data[0])

        self.keyPressFlag = False
        self.dragPicFlag = False
        self.showPosFlag = False
        self.selectedFlag = False
        self.editItemFlag = False
        self.currentIndex = 0
        # 点是否被选中的列表
        self.selectedFlagList = [False] * self.dataLength

        # self.activateMenu()
        # self.main_tabWidget = QTabWidget()
        # self.horizontalLayout.addWidget(self.main_tabWidget)

        # self.window.setMouseTracking(True)
        # self.centralwidget.setMouseTracking(True)
        #
        # self.main_tabWidget.setMouseTracking(True)
        self.canvasWidget = CanvasWidget()
        self.canvasLayout = QHBoxLayout()
        self.canvasLayout.addWidget(self.canvas)
        self.canvasWidget.setLayout(self.canvasLayout)

    def showTab(self):
        self.draw_lines.draw(*self.data)
        self.canvas.draw()

    def getCanvasWidget(self):
        return self.canvasWidget


# 操作canvas的类
class HMyCanvas():
    def __init__(self, canvas=None):
        self.canvas = canvas

    def setCanvas(self, canvas):
        self.canvas = canvas

    def showCanvas(self):
        pass


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


class ChangePointMenu(MyMenu):
    def __init__(self):
        MyMenu.__init__(self)
        self.editPos = QAction("编辑")
        self.insertAction(self.newPoint, self.editPos)


class MyPointMenu(QMenu):
    def __init__(self):
        super(QMenu, self).__init__()


class MyTableMenu(QMenu):
    def __init__(self):
        super(QMenu, self).__init__()


class MyWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()


# 包含canvas的控件
class CanvasWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

    # 设置右键要执行的函数
    def setContextMenuFunc(self, func):
        self.contextMenuFunc = func

    def contextMenuEvent(self, event) -> None:
        self.contextMenuFunc(event.globalPos())


# 包含canvas的控件
class CanvasContainer(QWidget):

    dataChangedSignal = pyqtSignal(list)
    tableUpdateSignal = pyqtSignal(dict)
    keyPressSignal = pyqtSignal(int)
    keyMoveSignal = pyqtSignal(dict)
    # 选择点时状态改变
    selectedChanged = pyqtSignal(dict)


    def __init__(self):
        super(QWidget, self).__init__()

        self.data = [[0], [0]]
        # self.data = [[0], [0]]
        # self.x, self.y = [1, 2, 6, 20, 30], [2, 20, 32, 35, 40]
        # self.data = [self.x, self.y]
        self.x, self.y = self.data
        # 记录鼠标在画布中的位置
        self.pos_x, self.pos_y = 0, 0
        self.dataLength = len(self.data[0])

        self.keyPressFlag = False
        self.dragPicFlag = False
        self.showPosFlag = False
        self.selectedPoints = []
        self.selectedPoint = ()
        # -1表示未选择，0表示放在上面未选中，-1表示选中了点
        self.selectState = -1

        self.editItemFlag = False
        self.currentIndex = 0
        # 点是否被选中的列表
        self.selectedFlagList = [False] * self.dataLength

        self.draw_lines = DrawLines()
        self.canvas = self.draw_lines.getCanvas()
        self.canvasLayout = QHBoxLayout()
        self.canvasLayout.addWidget(self.canvas)
        self.setLayout(self.canvasLayout)
        self.setMouseTracking(True)

        self.canvas.mpl_connect("motion_notify_event", self.keyMove)  # 鼠标移动触发事件
        self.canvas.mpl_connect("button_press_event", self.keyPress)  # 鼠标按下触发事件
        self.canvas.mpl_connect("button_release_event", self.keyRelease)  # 鼠标释放触发事件

    # 设置右键要执行的函数
    def setContextMenuFunc(self, func):
        self.contextMenuFunc = func

    def contextMenuEvent(self, event) -> None:
        self.contextMenuFunc(event.globalPos())

    def showCanvas(self, data=None):
        data = data if data else self.data
        # print("--------------data------------", data)
        self.draw_lines.draw(*data)
        self.canvas.draw()

    def keyPress(self, event):

        try:
            # 如果是左键按下
            if event.button == 1:
                # 不是双击左键
                if not event.dblclick:
                    self.keyPressFlag = True
                    # 如果鼠标放在点上面了
                    if self.selectState == 0:
                        self.selectState = 1
                        # print("---------selectedFlagList------------", self.selectedFlagList)
                        self.selectedFlagList[self.currentIndex] = not self.selectedFlagList[self.currentIndex]
                        # 如果这个点在选择的店里面
                        if self.selectedPoint in self.selectedPoints:
                            self.selectedPoints.pop(self.selectedPoints.index(self.selectedPoint))
                        else:
                            self.selectedPoints.append(self.selectedPoint)

                    elif self.selectedPoint:
                        self.selectState = -1
                        print("在别的区域选择")
                        self.selectedPoints = []
                        self.selectedFlagList = [False] * len(self.data[0])
                    else:
                        self.selectState = -2

                    self.selectedChanged.emit({"state": self.selectState, "points": self.selectedPoints})
                    # print("---------selectedFlagList------------", self.selectedFlagList)
                    self.updatePointColor()
        except Exception as ex:
            print("keyPressError: ", ex)

        finally:
            self.keyPressSignal.emit(event.button)

    def keyRelease(self, event):
        # print(event)
        if not event.dblclick:
            self.keyPressFlag = False
            if self.dragPicFlag:
                self.dragPicFlag = False
                self.dataChangedSignal.emit(self.data)

            elif self.selectState == 0:
                pass

    # 移动鼠标时改变状态栏信息，拖拽曲线
    def keyMove(self, event):
        try:
            self.pos_x, self.pos_y = event.xdata, event.ydata
            # 如果鼠标在画图区域内
            if self.pos_x and self.pos_y:
                dict = {"point_data": (event.xdata, event.ydata)}
                # 如果按钮按下且处于拖拽状态，直接画出线段
                if self.keyPressFlag and self.dragPicFlag:
                    self.data[0][self.currentIndex], self.data[1][self.currentIndex] = round(self.pos_x, 1), round(
                        self.pos_y, 1)
                    self.draw_lines.draw(*self.data)
                    self.selectedPoints = []
                    self.selectedChanged.emit({"state": -1, "points": self.selectedPoints})
                else:
                    # 如果已停止拖拽，鼠标移到点集附近时自动选中该点
                    index = 0
                    for x, y in zip(self.draw_lines.x, self.draw_lines.y):
                        if self.getPointDistance((x, y), (self.pos_x, self.pos_y)) < 0.5:
                            # 选取
                            self.selectState = 0
                            self.setCursor(Qt.CrossCursor)
                            self.selectedPoint = (x, y)
                            dict = {"point_data": self.selectedPoint}
                            self.currentIndex = index

                            if self.keyPressFlag:
                                self.dragPicFlag = True
                            else:
                                self.dragPicFlag = False
                            break
                        else:
                            # 未选中点时
                            self.selectState = -1
                            if self.dragPicFlag:
                                self.setCursor(Qt.CrossCursor)
                            else:
                                self.setCursor(Qt.ArrowCursor)
                        index += 1
                self.keyMoveSignal.emit(dict)
                if event.dblclick:
                    self.doubleClickFlag = True
            # 未移动到绘图区域时时
            else:
                self.keyMoveSignal.emit({"point_data": ()})
                self.selectState = -2
            self.selectedChanged.emit({"state": self.selectState, "points": self.selectedPoints})
        except Exception as ex:
            print("移动鼠标时发生错误: ", ex)

    def getPointDistance(self, p1, p2):
        dis = 0
        for i in range(len(p1)):
            dis += (p1[i]-p2[i])**2
        return dis**0.5

    # def showCanvas(self):
    #     self.dataChanged()
    #     self.draw_lines.draw(self.x, self.y)
    #     # 设置布局
    #     self.canvas.draw()

    def showMaskPoint(self, flag):
        if not flag:
            self.draw_lines.scatterPart.remove()
            self.draw_lines.scatterPart = None
        else:
            self.updatePointColor()
        self.canvas.draw()

    def updatePointColor(self):
        self.draw_lines.updateScatter(self.selectedFlagList)
        self.canvas.draw()

    # def dataChanged(self):
    #     self.dataChangedSignal.emit(self.data)

    # 改变点或者新增点, flag为0表示编辑点，flag为+1表示增加点, -1 表示删除点
    def updatePointPos(self, flag, data=None):
        print("新增点", data)
        if data:
            if flag == 0:
                # 替换点坐标
                self.data[0][self.currentIndex], self.data[1][self.currentIndex] = data
                index = self.currentIndex
                self.tableUpdateSignal.emit({"flag": flag, "data": data, "index": index, "rows": None})

            elif flag == 1:
                index = self.currentIndex + 1 if True in self.selectedFlagList else self.dataLength
                self.data[0].insert(index, data[0])
                self.data[1].insert(index, data[1])
                self.dataLength += 1
                print("进入table的点", data, index)
                self.tableUpdateSignal.emit({"flag": flag, "data": data, "index": index, "rows": None})
                print("-=-=-=-=")
        elif flag == -1:
            # print("-----------delete---------------")
            index_list = [index for index in range(self.dataLength) if self.selectedFlagList[index]]
            x = [self.data[0][index] for index in range(self.dataLength) if index not in index_list]
            y = [self.data[1][index] for index in range(self.dataLength) if index not in index_list]
            # self.selectedFlagList = [self.selectedFlagList[index] for index in range(self.dataLength) if
            #                          index not in index_list]
            self.data = [x, y]
            self.dataLength = len(self.data[0])
            # print("------------x--------------", x)
            self.tableUpdateSignal.emit({"flag": flag, "data": None, "index": None, "rows": index_list})

        self.selectedFlagList = [False] * (self.dataLength)
        # print("---------selectedFlagList------------", self.selectedFlagList)
        self.selectedPoints = []
        self.selectedChanged.emit({"state": -1, "points": self.selectedPoints})
        self.draw_lines.draw(*self.data)

    def resetPointState(self):
        self.selectedFlagList = [False] * len(self.data[0])
        self.draw_lines.draw(*self.data)

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def getFigure(self):
        return self.draw_lines.getFigure()


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
            warning_box = QMessageBox(QMessageBox.Warning, "警告","输入非小数", QMessageBox.Ok)
            warning_box.exec_()
            return None

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.closeFunc()


class Ui_MyWindow(Ui_MainWindow):

    def __init__(self, mainWindow):

        self.window = mainWindow
        self.setupUi(self.window)

    def setupUi(self, Window):
        super(Ui_MyWindow, self).setupUi(Window)
        self.canvasWidgetList = []
        self.canvasWidget = None
        self.autoSwitchFlag = True

        self.main_tabWidget = QTabWidget()
        self.main_tabWidget.setMouseTracking(True)

        self.horizontalLayout.addWidget(self.main_tabWidget)
        self.dockWidget.setFeatures(QDockWidget.AllDockWidgetFeatures)

        self.window.setMouseTracking(True)
        self.centralwidget.setMouseTracking(True)
        self.main_tabWidget.setMouseTracking(True)

        self.tabAddBtn = QPushButton()
        self.tabAddBtn.setIcon(getIcon(":resources//MyIcon//plus-circle-fill.svg"))
        self.tabAddBtn.setFlat(False)
        self.tabAddBtn.clicked.connect(self.addPage)

        self.main_tabWidget.setCornerWidget(self.tabAddBtn, Qt.TopLeftCorner)
        self.main_tabWidget.setTabsClosable(True)
        self.main_tabWidget.tabCloseRequested.connect(self.closeCurrentTab)
        self.main_tabWidget.currentChanged.connect(self.setCurrentTab)

        # 设置表格行列宽度
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # 设置events_table的右键菜单
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.showTableMenu)

        canvasContainer = CanvasContainer()
        self.canvasWidgetList.append(canvasContainer)
        self.currentCanvasWidget = canvasContainer
        self.main_tabWidget.addTab(self.currentCanvasWidget, "tab0")

        self.process_data = processData()
        self.setCanvasWidget()

        self.process_data.setData(self.data)
        self.action.triggered.connect(lambda: self.process_data.saveData())
        self.action_2.triggered.connect(lambda: self.process_data.exportData())
        self.process_data.getUpdateFunc([self.exportDataToTable, self.getTableData])

        self.checkBox_2.setCheckState(Qt.Checked)

    def setCanvasWidget(self):
        # 鼠标所在位置的数据点
        self.point_data = ()
        # 记录鼠标在状态栏中的位置
        self.selectedPoint = ()

        self.selectState = -1
        self.showPosFlag = False

        self.editItemFlag = False
        self.selectedPoints = []
        self.currentIndex = 0
        # 点是否被选中的列表
        self.selectedFlagList = [False]

        # self.currentCanvasWidget.setContextMenuFunc(self.showContextMenu)
        self.currentCanvasWidget.dataChangedSignal[list].connect(self.updateData)
        self.currentCanvasWidget.keyMoveSignal[dict].connect(self.updatePointData)
        self.currentCanvasWidget.tableUpdateSignal[dict].connect(self.updateMyTable)
        self.currentCanvasWidget.selectedChanged[dict].connect(self.updateSelectState)
        self.currentCanvasWidget.setContextMenuFunc(self.showContextMenu)
        self.checkBox_2.stateChanged[int].connect(self.showMaskPoint)

        self.data = self.currentCanvasWidget.getData()
        print("转换tab的data", self.data)
        self.exportDataToTable(self.data)
        self.process_data.setFig(self.currentCanvasWidget.getFigure())
        self.currentCanvasWidget.showCanvas()

    def showMaskPoint(self, state):
        flag = True if state == 2 else False
        self.currentCanvasWidget.showMaskPoint(flag)


    def updateData(self, data):
        self.data = data
        self.exportDataToTable(self.data)

    def updateSelectState(self, selectState):
        self.selectState = selectState["state"]
        self.selectedPoints = selectState["points"]
        message1 = ""
        if self.selectedPoints:
            for point in self.selectedPoints:
                message1 +=  "、 " + "x :" + str(point[0]) + ", y :" + str(point[1])
            message1 = "已选择" + message1
        # print("----------------")
        # print(self.selectState)
        # 显示鼠标所在点的数据
        if self.selectState == 1:
            message2 = ""
        # 没有点可选择
        elif self.selectState == -2:
            message2 = "没有点可选择！"
        else:
            message2 = "正在选择 " + "x :" + str(round(self.point_data[0], 3)) + \
                                  ", y :" + str(round(self.point_data[1], 3)) + "  "
        self.statusbar.showMessage(message2+message1)
        # print("====")

    def updatePointData(self, kwargs):
        self.point_data = kwargs["point_data"]
        self.currentIndex = self.currentCanvasWidget.currentIndex

    # def updateData(self, data):
    #     self.data = data
    #     # print(self.data, "------")
    #     self.exportDataToTable(self.data)

    def getFunc(self, func, *args, **kwargs):
        self.myFunc = func
        self.dictArgs = kwargs
        self.tupleArgs = args

    # 双击时创建可以输入位置坐标的，此处x, y 是相对于窗口坐标，不是具体坐标轴中的坐标
    def showPosInput(self, flag):
        if not self.showPosFlag and self.point_data:
            texts = [round(self.point_data[0], 3), round(self.point_data[1], 3)]
            x, y = (QCursor.pos().x(), QCursor.pos().y())
            self.posWidget = InputPointWdt()
            self.posWidget.move(x-120, y-20)
            self.posWidget.setLineEditText(*texts)
            self.posWidget.show()
            self.showPosFlag = True
            self.posWidget.setCloseFunc(self.closePosInput)
            print("========show pos=========")
            self.posWidget.okBtn.clicked.connect(lambda: self.updatePointPos(flag))

    # 展示右键菜单
    def showContextMenu(self, pos):
        self.point_menu = ChangePointMenu()
        self.point_menu.editPos.triggered.connect(lambda: self.showPosInput(0))
        self.point_menu.newPoint.triggered.connect(lambda: self.showPosInput(1))
        self.point_menu.delete.triggered.connect(lambda: self.updatePointPos(-1))
        flag = False if self.selectedPoints==[] else True
        self.point_menu.editPos.setEnabled(flag)
        self.point_menu.delete.setEnabled(flag)
        self.point_menu.exec_(pos)

    # 关闭输入框
    def closePosInput(self):
        if self.showPosFlag:
            self.showPosFlag = False

    # 改变点或者新增点, flag为0表示编辑点，flag为+1表示增加点， -1为删除点
    def updatePointPos(self, flag):
        if flag != -1:
            data = self.posWidget.getData()
            if data:
                self.posWidget.close()
        else:
            data = None
        self.currentCanvasWidget.updatePointPos(flag, data)

    # 提醒保存
    def closeCurrentTab(self):
        response_btn =  QMessageBox.warning(self.window, "保存提示", "是否保存？", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        if response_btn == QMessageBox.Yes:
            self.process_data.saveData()
        self.main_tabWidget.removeTab(self.main_tabWidget.currentIndex())
        self.canvasWidgetList.pop(self.main_tabWidget.currentIndex())

    def setCurrentItem(self, row, col):
        self.editItemFlag = True
        self.currentItemText = self.tableWidget.item(row, col).text()

    def checkTableInput(self, row, col):
        try:
            print("新增行{} 列{}".format(row, col))
            # 如果是由表格的右键菜单引起的项目内容变化，不检查其值
            # print(self.tableWidget.item(row, col).text())
            if self.editItemFlag:
                temp = float(self.tableWidget.item(row, col).text())
                self.data = self.getTableData()
                self.currentCanvasWidget.showCanvas(self.data)
            self.editItemFlag = False
        except Exception as ex:
            print("这里有问题", ex)
            response_btn = QMessageBox.warning(self.tableWidget, "输入错误", "请输入一个小数！", QMessageBox.Yes)
            self.tableWidget.item(row, col).setText(self.currentItemText)

    def exportDataToTable(self, data=[]):
        self.statusbar.showMessage("表格数据导入中")
        # print(len(data))
        if len(data[0]) == 0:
            QMessageBox.information(self.window, "导入数据为空","数据为空", QMessageBox.Ok)
            return False
        rows, cols = len(data[0]), len(data)
        print("导入数据时的大小", rows, cols)
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(cols)
        for row in range(rows):
            for col in range(cols):
                item = QTableWidgetItem()
                item.setText(str(data[col][row]))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(row, col, item)
        self.statusbar.showMessage("表格数据导入完成！")
        print("-----------export------------")
        self.tableWidget.cellDoubleClicked.connect(self.setCurrentItem)
        self.tableWidget.cellChanged.connect(self.checkTableInput)
        return True

    def getTableData(self):
        print("---------------正在保存信息-------------------")
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
        self.process_data.setData(data_list)
        self.statusbar.showMessage("保存完成！")
        return data_list

    # flag: 0修改， 1， 增加， -1， 删除
    def updateMyTable(self, kwargs):
        flag = kwargs["flag"]
        data = kwargs["data"]
        index = kwargs["index"]
        rows = kwargs["rows"]

        # print("--------------update Table-----------------")
        index = len(self.data[0]) - 1 if not index else index
        if flag == 0:
            x, y = data
            self.tableWidget.item(index, 0).setText(str(x))
            self.tableWidget.item(index, 1).setText(str(y))

        elif flag == 1:
            x, y = data
            # self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
            self.tableWidget.insertRow(index)
            # print(self.tableWidget.columnCount(), self.tableWidget.rowCount())
            # self.tableWidget.item(index, 0).setText(str(x))
            # self.tableWidget.item(index, 1).setText(str(x))
            # self.tableWidget.item(index, 0).setTextAlignment(Qt.AlignCenter)
            # self.tableWidget.item(index, 1).setTextAlignment(Qt.AlignCenter)

            x_item = QTableWidgetItem()
            y_item = QTableWidgetItem()
            x_item.setTextAlignment(Qt.AlignCenter)
            y_item.setTextAlignment(Qt.AlignCenter)
            x_item.setText(str(x))
            y_item.setText(str(y))
            self.tableWidget.setItem(index, 0, x_item)
            self.tableWidget.setItem(index, 1, y_item)
            # print(self.tableWidget.columnCount(), self.tableWidget.rowCount())
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

    # 新增点或者删除点
    def changeTableData(self, flag):
        self.tableMenuFlag = True
        index = set()
        if not self.tableWidget.selectedItems():
            index.add(self.tableWidget.rowCount() - 1)
        else:
            for item in self.tableWidget.selectedItems():
                index.add(item.row())
        index = list(index)
        kwargs = {"flag": 1, }
        if flag:
            kwargs = {"flag": 1, "data": [0, 0], "index": index[0]+1, "rows": list(index)}
        else:
            kwargs = {"flag": -1, "data": None, "index": None, "rows": list(index)}
        self.updateMyTable(kwargs)
        self.data = self.getTableData()
        self.currentCanvasWidget.setData(self.data)
        self.currentCanvasWidget.resetPointState()

    def createNewTab(self):
        pass

    def addPage(self):
        self.autoSwitchFlag = True
        canvasWidget = CanvasContainer()
        self.canvasWidgetList.append(canvasWidget)
        index = self.main_tabWidget.currentIndex()+1
        self.main_tabWidget.addTab(canvasWidget, "tab"+str(index))
        self.main_tabWidget.setCurrentIndex(index)

        self.currentCanvasWidget.dataChangedSignal[list].disconnect(self.updateData)
        self.currentCanvasWidget.keyMoveSignal[dict].disconnect(self.updatePointData)
        self.currentCanvasWidget.tableUpdateSignal[dict].disconnect(self.updateMyTable)
        self.currentCanvasWidget.selectedChanged[dict].disconnect(self.updateSelectState)
        self.checkBox_2.stateChanged[int].disconnect(self.showMaskPoint)


        self.currentCanvasWidget = canvasWidget
        self.currentCanvasWidget.getFigure().clf()
        self.setCanvasWidget()
        # 新建时设置自动切换到该

    def setCurrentTab(self, index):
        if not self.autoSwitchFlag:

            self.data = self.getTableData()
            self.currentCanvasWidget.setData(self.data)
            self.currentCanvasWidget.getFigure().clf()

            self.currentCanvasWidget.dataChangedSignal[list].disconnect(self.updateData)
            self.currentCanvasWidget.keyMoveSignal[dict].disconnect(self.updatePointData)
            self.currentCanvasWidget.tableUpdateSignal[dict].disconnect(self.updateMyTable)
            self.currentCanvasWidget.selectedChanged[dict].disconnect(self.updateSelectState)
            self.checkBox_2.stateChanged[int].disconnect(self.showMaskPoint)
            self.currentCanvasWidget = self.canvasWidgetList[index]

            self.setCanvasWidget()
        self.autoSwitchFlag = False




# 运行程序
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyWindow()
    ui_window = Ui_MyWindow(main_window)
    main_window.show()
    app.exec()




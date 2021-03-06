# import matplotlib
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import numpy as np
import sys
from GUI.mainWindow import Ui_MainWindow
from GUI.settings import Ui_Dialog
from drawCurves.DrawCurves import *
from Data.processExcel import *
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import  QRegExpValidator
import math
import time
import src

def getIcon(path):
    file_pixmap = QPixmap(path)
    file_fit_pixmap = file_pixmap.scaled(16, 16, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    # 注意 scaled() 返回一个 QPixmap
    return QIcon(file_fit_pixmap)


class SetMyDialog(QObject):

    changeSettingSignal = pyqtSignal(dict)

    def __init__(self, settingsDict):
        super(QObject, self).__init__()

        self.dialog = QDialog()
        self.settingsDict = settingsDict
        # self.settingsDict = {
        #
        #                     "point": {},
        #                      "line": {},
        #                      "axes": {
        #                               "autoScale": True,
        #                               "title": "",
        #                               "x_min": 0,
        #                               "x_max": 10,
        #                               "y_min": 0,
        #                               "y_max": 10,
        #                               "x_tick": 1,
        #                               "y_tick": 1
        #                      },
        #                      "font": {"size": 2,
        #                               "family": "宋体",
        #                               "color": "#000000"},
        #                      "bezier": {}
        #                      }
        # self.settingsDict["point"] = {
        #                   "color": "#182C61",
        #                    "style": ".",
        #                    "size": 1,
        #                  }
        # self.settingsDict["bezier"] = {
        #                   "color": "#6D214F",
        #                   "style": "-",
        #                   "width": 1,
        #                   }
        #
        # self.settingsDict["line"] = {
        #                   "color": "#82589F",
        #                   "style": "-",
        #                   "width": 1,
        #                 }
        self.lineDict = {
            "-": "------",
            "------": "-",
            "-.-.-.": "-.",
            "-.": "-.-.-.",
            "......": "--",
            "--": "......"
                }
        self.setupUi()


    def setupUi(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.dialog)
        self.dialog.setWindowModality(Qt.ApplicationModal)

        validator = QDoubleValidator(self.dialog)
        validator.setDecimals(3)
        self.ui.lineEdit_2.setValidator(validator)
        self.ui.lineEdit_3.setValidator(validator)
        self.ui.lineEdit_4.setValidator(validator)
        self.ui.lineEdit_5.setValidator(validator)
        self.ui.yLineEdit.setValidator(validator)
        self.ui.yLineEdit_2.setValidator(validator)

        self.updateValue()

        self.ui.set_lineColor_btn.clicked.connect(lambda: self.selectColor(self.ui.set_lineColor_btn, "line"))
        self.ui.set_pointColor_btn.clicked.connect(lambda: self.selectColor(self.ui.set_pointColor_btn, "point"))
        self.ui.pushButton_7.clicked.connect(lambda: self.selectColor(self.ui.pushButton_7, "font"))
        self.ui.pushButton.clicked.connect(lambda: self.changeSettings())
        self.ui.pushButton_2.clicked.connect(lambda: self.dialog.close())
        self.ui.CheckBox.stateChanged.connect(self.editAxesRange)
        self.showAxesLineEdit(False)

        self.ui.lineEdit_2.textChanged.connect(lambda: self.setAxesRange(text="x_min"))
        self.ui.lineEdit_3.textChanged.connect(lambda: self.setAxesRange(text="x_max"))
        self.ui.lineEdit_4.textChanged.connect(lambda: self.setAxesRange(text="y_min"))
        self.ui.lineEdit_5.textChanged.connect(lambda: self.setAxesRange(text="y_max"))

        self.updateSliderRange()
        self.ui.horizontalSlider.valueChanged.connect(self.updateXTick)
        self.ui.horizontalSlider_2.valueChanged.connect(self.updateYTick)
        self.ui.yLineEdit.textChanged.connect(self.updateXSliderValue)
        self.ui.yLineEdit_2.textChanged.connect(self.updateYSliderValue)
        self.ui.comboBox_2.currentIndexChanged.connect(self.setLines)

    def setLines(self, index):
        print(index)
        prior_curve = "line" if index == 1 else "bezier"
        current_curve = "line" if index == 0 else "bezier"
        self.settingsDict[prior_curve]["width"] = self.ui.spinBox_3.value()
        self.settingsDict[prior_curve]["style"] = self.lineDict[self.ui.comboBox.currentText()]

        self.ui.set_lineColor_btn.\
                setStyleSheet('''QPushButton {{ 
                                background-color: {0}; 
                                }}'''.format(self.settingsDict[current_curve]["color"]))

        self.ui.spinBox_3.setValue(self.settingsDict[current_curve]["width"])
        self.ui.comboBox.setCurrentText(self.lineDict[self.settingsDict[current_curve]["style"]])

    def updateValue(self):
        curve = self.settingsDict["line"] if self.ui.comboBox_2.currentIndex() == 0 else self.settingsDict["bezier"]
        self.ui.spinBox_3.setValue(int(curve["width"]))

        self.ui.set_lineColor_btn.\
            setStyleSheet('''QPushButton {{ 
                                background-color: {0}; 
                                }}'''.format(curve["color"]))

        self.ui.comboBox.setCurrentText(str(self.lineDict[curve["style"]]))

        self.ui.spinBox_4.setValue(int(self.settingsDict["point"]["size"]))
        self.ui.set_pointColor_btn.\
            setStyleSheet('''QPushButton {{ 
                                background-color: {0}; 
                                }}'''.format(self.settingsDict["point"]["color"]))
        self.ui.comboBox_3.setCurrentText(str(self.settingsDict["point"]["style"]))

        self.ui.lineEdit.setText(self.settingsDict["axes"]["title"])
        self.ui.spinBox_5.setValue(int(self.settingsDict["font"]["size"]))

        self.ui.pushButton_7.setStyleSheet('''QPushButton {{ 
                                background-color: {0}; 
                                }}'''.format(self.settingsDict["font"]["color"]))

        state = Qt.Checked if self.settingsDict["axes"]["autoScale"] else Qt.Unchecked
        self.ui.CheckBox.setCheckState(state)
        ax = self.settingsDict["axes"]
        self.ui.lineEdit_2.setText(str(ax["x_min"]))
        self.ui.lineEdit_3.setText(str(ax["x_max"]))
        self.ui.lineEdit_4.setText(str(ax["y_min"]))
        self.ui.lineEdit_5.setText(str(ax["y_max"]))
        self.ui.yLineEdit.setText(str(ax["x_tick"]))
        self.ui.yLineEdit_2.setText(str(ax["y_tick"]))
        if self.settingsDict["axes"]["autoScale"]:
            self.ui.CheckBox.setCheckState(Qt.Checked)
        else:
            self.ui.CheckBox.setCheckState(Qt.Unchecked)
            self.editAxesRange(True)

    def updateAxesSetting(self):
        x_min = self.settingsDict["axes"].get("x_min", 0)
        x_max = self.settingsDict["axes"].get("x_max", 10)
        y_min = self.settingsDict["axes"].get("y_min", 0)
        y_max = self.settingsDict["axes"].get("y_max", 10)

        self.ui.horizontalSlider.setMinimum(int(x_min * 1000))
        self.ui.horizontalSlider.setMaximum(int(x_max * 1000))
        x_tick = (int(x_max * 1000) - int(x_min * 1000)) // 100
        self.ui.horizontalSlider.setSingleStep(x_tick)
        self.ui.horizontalSlider_2.setMinimum(int(y_min * 1000))
        self.ui.horizontalSlider_2.setMaximum(int(y_max * 1000))
        y_tick = (int(y_max * 1000) - int(y_min * 1000)) // 100
        self.ui.horizontalSlider_2.setSingleStep(y_tick)

        self.ui.lineEdit_2.setText(str(x_min))
        self.ui.lineEdit_3.setText(str(x_max))
        self.ui.lineEdit_4.setText(str(y_min))
        self.ui.lineEdit_5.setText(str(y_max))

        self.ui.yLineEdit.setText(str(x_tick))
        self.ui.yLineEdit_2.setText(str(y_tick))

        self.settingsDict["axes"]["x_min"] = x_min
        self.settingsDict["axes"]["x_max"] = x_max
        self.settingsDict["axes"]["y_min"] = y_min
        self.settingsDict["axes"]["y_max"] = y_max
        self.settingsDict["axes"]["x_tick"] = self.ui.yLineEdit.text()
        self.settingsDict["axes"]["y_tick"] = self.ui.yLineEdit_2.text()

    def updateXTick(self, value):
        self.ui.yLineEdit.setText(str(value/1000))

    def updateYTick(self, value):
        self.ui.yLineEdit_2.setText(str(value/1000))

    def updateXSliderValue(self, text):
        self.ui.horizontalSlider.setValue(int(float(text)*1000))

    def updateYSliderValue(self, text):
        self.ui.horizontalSlider_2.setValue(int(float(text)*1000))

    def setAxesRange(self, text=""):
        self.settingsDict["axes"][text] = float(self.sender().text())
        self.updateSliderRange()

    def updateSliderRange(self):
        x_min = self.settingsDict["axes"].get("x_min", 0)
        x_max = self.settingsDict["axes"].get("x_max", 10)
        y_min = self.settingsDict["axes"].get("y_min", 0)
        y_max = self.settingsDict["axes"].get("y_max", 10)
        self.ui.horizontalSlider.setMinimum(int(x_min*1000))
        self.ui.horizontalSlider.setMaximum(int(x_max*1000))
        x_tick = (int(x_max*1000) - int(x_min*1000)) // 100
        self.ui.horizontalSlider.setSingleStep(x_tick)
        self.ui.horizontalSlider_2.setMinimum(int(y_min*1000))
        self.ui.horizontalSlider_2.setMaximum(int(y_max*1000))
        y_tick = (int(y_max*1000) - int(y_min*1000)) // 100
        self.ui.horizontalSlider_2.setSingleStep(y_tick)

        self.settingsDict["axes"]["x_min"] = x_min
        self.settingsDict["axes"]["x_max"] = x_max
        self.settingsDict["axes"]["y_min"] = y_min
        self.settingsDict["axes"]["y_max"] = y_max
        self.settingsDict["axes"]["x_tick"] = self.ui.yLineEdit.text()
        self.settingsDict["axes"]["y_tick"] = self.ui.yLineEdit_2.text()

    def showAxesLineEdit(self, flag):
        self.settingsDict["axes"]["autoScale"] = flag
        self.ui.lineEdit_2.setVisible(flag)
        self.ui.lineEdit_3.setVisible(flag)
        self.ui.lineEdit_4.setVisible(flag)
        self.ui.lineEdit_5.setVisible(flag)
        self.ui.yLineEdit.setVisible(flag)
        self.ui.yLineEdit_2.setVisible(flag)
        self.ui.Label_2.setVisible(flag)
        self.ui.label_2.setVisible(flag)
        self.ui.label_3.setVisible(flag)
        self.ui.horizontalSlider.setVisible(flag)
        self.ui.horizontalSlider_2.setVisible(flag)
        self.ui.label.setVisible(flag)
        self.ui.label_13.setVisible(flag)
        self.ui.yLabel.setVisible(flag)

    def editAxesRange(self, state):
        flag = True if state == 2 else False

        self.showAxesLineEdit(not flag)

    def changeSettings(self):

        self.settingsDict["point"]["size"] = self.ui.spinBox_4.value()
        self.settingsDict["point"]["style"] = self.ui.comboBox_3.currentText()
        self.settingsDict["axes"]["title"] = self.ui.lineEdit.text()
        self.settingsDict["font"]["size"] = self.ui.spinBox_5.value()
        self.settingsDict["axes"]["x_tick"] = self.ui.yLineEdit.text()
        self.settingsDict["axes"]["y_tick"] = self.ui.yLineEdit_2.text()
        current_curve = "line" if self.ui.comboBox_2.currentIndex() == 0 else "bezier"
        self.settingsDict[current_curve]["width"] = self.ui.spinBox_3.value()
        self.settingsDict[current_curve]["style"] = self.lineDict[self.ui.comboBox.currentText()]
        self.settingsDict["axes"]["autoScale"] = True if self.ui.CheckBox.isChecked() else False
        self.changeSettingSignal.emit(self.settingsDict)
        # print(self.settingsDict)
        self.dialog.close()

    def getSettings(self):
        pass
        return self.settingsDict

    def selectColor(self, btn, name):
        color = QColorDialog.getColor(Qt.blue, self.dialog, "选择"+name+ "颜色")
        if color.isValid():
            # 双重大括号表示转义
            self.sender().\
                setStyleSheet('''QPushButton {{ 
                                background-color: {0}; 
                                }}'''.format(color.name()))
            if name == "line":
                if self.ui.comboBox.currentIndex == 0:
                    self.settingsDict["bezier"]["color"] = color.name()
                else:
                    self.settingsDict["line"]["color"] = color.name()
            else:
                self.settingsDict[name]["color"] = color.name()


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

    updatePlotArgs = pyqtSignal(dict)
    dataChangedSignal = pyqtSignal(list)
    tableUpdateSignal = pyqtSignal(dict)
    keyPressSignal = pyqtSignal(int)
    keyMoveSignal = pyqtSignal(dict)
    doubleClicked = pyqtSignal(bool)
    # 选择点时状态改变
    selectedChanged = pyqtSignal(dict)

    def __init__(self):
        super(QWidget, self).__init__()

        self.data = [[0], [0]]
        # self.data = [[0], [0]]
        # self.x, self.y = [1, 2, 6, 20, 30], [2, 20, 32, 35, 40]
        # self.data = [self.x, self.y]
        self.plotArgsDict = {  # 设置图例位置
                            "axes1": {}
                            }

        self.plotArgsDict["axes1"] = {
            "legend": {},
            "line1": {},
            "curve1": {},
            "scatter1": {},
            "lim": [],  # x, y 轴的最大最小值
            "tick": [[], []],  # x, y 轴的刻度
            "title": (),  # x, y 轴的标题
            "auto_scaled": True  # 自动缩放刻度
        }
        self.plotArgsDict["axes1"]["legend"] = {"isVisible": True,  # 设置是否可见
                                                "loc": (0.9, 0.9),  # 设置相对位置
                                                "pos": (0.9, 0.9),  # 设置绝对位置
                                                }

        self.plotArgsDict["axes1"]["line1"] = {"label": "line1",
                                              "color": 'r',
                                              "ls": '-',
                                              }

        self.x, self.y = self.data
        self.dataLength = len(self.data[0])

        self.keyPressFlag = False
        self.dragPicFlag = False
        self.dragLegendFlag = False
        self.showPosFlag = False
        self.selectedPoints = []
        self.selectedPoint = ()
        # 画图的字典
        self.plotArgs = {}
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

        self.draw_lines.updatePlotArgs[dict].connect(self.setPlotArgs)
        self.updatePlotArgs[dict].connect(self.draw_lines.setPlotArgs)

    def setPlotArgs(self, kwargs={}):
        self.plotArgsDict = dict(self.plotArgsDict, **kwargs)
        ax = self.plotArgsDict["axes1"]
        if ax["auto_scaled"]:
            if len(self.data[0]) > 1:
                # print("-------------->2-----------")
                min_x, max_x = min(self.data[0]), max(self.data[0])
                min_y, max_y = min(self.data[1]), max(self.data[1])
                x_diff = max_x - min_x
                y_diff = max_y - min_y
                x_lim = (min_x - 0.1 * x_diff, max_x + 0.1 * x_diff)
                y_lim = (min_y - 0.1 * y_diff, max_y + 0.1 * y_diff)

            elif len(self.data[0]) == 1 and self.data[0][0] != 0:
                x_lim = (self.data[0][0] - 0.1 * abs(self.data[0][0]), self.data[0][0] + 0.1 * abs(self.data[0][0]))
                y_lim = (self.data[1][0] - 0.1 * abs(self.data[1][0]), self.data[1][0] + 0.1 * abs(self.data[1][0]))

            else:
                x_lim = (-10, 10)
                y_lim = (-10, 10)
            # print(x_lim, y_lim)
            ax["lim"] = [x_lim, y_lim]
            ax["tick"] = [np.arange(x_lim[0], x_lim[1] + 0.1 * (x_lim[1] - x_lim[0]), 0.1 * (x_lim[1] - x_lim[0])), \
                          np.arange(y_lim[0], y_lim[1] + 0.1 * (y_lim[1] - y_lim[0]), 0.1 * (y_lim[1] - y_lim[0]))]
            self.updatePlotArgs.emit(self.plotArgsDict)

    # 设置右键要执行的函数
    def setContextMenuFunc(self, func):
        self.contextMenuFunc = func

    def contextMenuEvent(self, event) -> None:
        self.contextMenuFunc(event.globalPos())

    def showCanvas(self, data=None):
        self.data = data if data else self.data
        # print("--------------data------------", data)
        self.setPlotArgs()
        self.draw_lines.draw(*self.data)
        self.canvas.draw()

    def keyPress(self, event):

        try:
            # 如果是左键按下
            if event.button == 1:
                if event.dblclick:
                    print(event)
                    # 状态为0
                    if self.selectState == 0:
                        self.doubleClicked.emit(True)
                    else:
                        self.doubleClicked.emit(False)
                # 不是双击左键
                else:
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

                    elif self.selectState == 2:
                        pass

                    elif self.selectedPoint:
                        self.selectState = -1
                        # print("在别的区域选择")
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
            elif self.dragLegendFlag:
                self.dragLegendFlag = False

            elif self.selectState == 0:
                pass

    # 图例的绝对坐标和相对坐标之间的换算
    def getLegendPos(self, flag, pos=()):
        res = ()
        x_lim, y_lim = self.plotArgsDict["axes1"]["lim"]
        legend = self.plotArgsDict["axes1"]["legend"]
        if flag:
            loc = legend["loc"]
            # 计算legend的绝对尺寸
            x_legend = x_lim[0] + (x_lim[1] - x_lim[0]) * loc[0]
            y_legend = y_lim[0] + (y_lim[1] - y_lim[0]) * loc[1]
            res = (x_legend, y_legend)
        else:
            x_loc = (pos[0] - x_lim[0]) / (x_lim[1] - x_lim[0])
            y_loc = (pos[1] - y_lim[0]) / (y_lim[1] - y_lim[0])
            res = (x_loc-0.05, y_loc-0.05)
            legend["loc"] = res
            self.setPlotArgs()
            # print(self.plotArgsDict)
        return res

    # 判断鼠标是否进入legend区域
    def enterLegend(self, pos):
        legend = self.plotArgsDict["axes1"]["legend"]
        x_legend, y_legend = self.getLegendPos(True)
        # print(x_legend, y_legend)
        if legend["isVisible"]:
            if pos[0] > x_legend and pos[0] < x_legend + 0.3*abs(x_legend) and \
                            pos[1] > y_legend and pos[1] < y_legend + 0.3*abs(y_legend):
                self.setCursor(Qt.SizeAllCursor)
                return True
        return False


        # print("----------pos: {}, x_lim: {}, y_lim: {} loc: {}".format(pos, x_lim, y_lim, loc))

    # 移动鼠标时改变状态栏信息，拖拽曲线
    def keyMove(self, event):
        try:
            x_data, y_data = event.xdata, event.ydata
            # 如果鼠标在画图区域内
            if x_data and y_data:

                dict = {"point_data": (event.xdata, event.ydata)}
                # 如果按钮按下且处于拖拽状态，直接画出线段
                if self.keyPressFlag and self.dragPicFlag:
                    self.data[0][self.currentIndex], self.data[1][self.currentIndex] = round(x_data, 3), round(y_data, 3)
                    self.setPlotArgs()
                    self.selectedPoints = []
                    self.selectedChanged.emit({"state": -1, "points": self.selectedPoints})
                    self.draw_lines.updateCanvas(*self.data)
                else:
                    self.selectState = -1
                    self.setPlotArgs()
                    #
                    # if self.keyPressFlag and self.dragLegendFlag:
                    #     # print("-----------drag legend--------")
                    #     self.getLegendPos(False, (x_data, y_data))
                    #     self.setCursor(Qt.SizeAllCursor)
                    #     self.draw_lines.updateLegend()
                    #     self.canvas.draw()
                    #
                    # # 如果放在legend上
                    # elif self.enterLegend((x_data, y_data)):
                    #     # print("-----------drag legend2--------")
                    #     self.selectState = 2
                    #     if self.keyPressFlag:
                    #         self.dragLegendFlag = True

                    # 看是否放在上面
                    if len(self.data[0]) == 1:
                        if self.data[0][0] == 0 and self.data[1][0] == 0:
                            if self.getPointDistance((x_data, y_data), (0, 0)) < 0.05:
                                self.selectState = 0
                                self.selectedPoint = (0, 0)
                                self.currentIndex = 0
                        else:
                            if abs(x_data-self.data[0]) <= abs(self.data[0][0])/100 or abs(y_data-self.data[1]) <= abs(self.data[1][0]/100):
                                self.selectState = 0
                                self.selectedPoint = (self.data[0], self.data[1])
                                self.currentIndex = 0

                    elif  len(self.data[0]) == 0:
                        pass

                    else:
                        index = 0
                        x_diff, y_diff = max(self.data[0])-min(self.data[0]), max(self.data[1])-min(self.data[1])
                        for x, y in zip(self.data[0], self.data[1]):
                            if abs(x_data - x) <= x_diff/100 and abs(y_data - y) <= y_diff/100:
                                self.selectState = 0
                                self.selectedPoint = (x, y)
                                self.currentIndex = index
                                break
                            index += 1

                    # 如果放在已有点上
                    if self.selectState == 0:
                        self.setCursor(Qt.CrossCursor)
                        dict = {"point_data": self.selectedPoint}
                        self.dragPicFlag = True if self.keyPressFlag else False

                    elif self.selectState == 2:
                        self.setCursor(Qt.SizeAllCursor)

                    else:
                        # 未选中点时
                        self.selectState = -1
                        if self.dragPicFlag:
                            self.setCursor(Qt.CrossCursor)
                        else:
                            self.setCursor(Qt.ArrowCursor)

                    self.keyMoveSignal.emit(dict)

                if event.dblclick:
                    self.doubleClickFlag = True
            # 未移动到绘图区域时时
            else:
                if self.keyPressFlag and self.dragPicFlag:
                    self.keyPressFlag = False
                    self.dragPicFlag = False
                    self.dataChangedSignal.emit(self.data)
                    self.setCursor(Qt.ArrowCursor)
                else:
                    self.keyMoveSignal.emit({"point_data": ()})
                    self.selectState = -2

            self.selectedChanged.emit({"state": self.selectState, "points": self.selectedPoints})
        except Exception as ex:
            print("移动鼠标时发生错误: ", ex)

    def updateLegend(self):
        pass

    def getPointDistance(self, p1, p2):
        dis = 0
        for i in range(len(p1)):
            dis += (p1[i]-p2[i])**2
        return dis**0.5

    def showMaskPoint(self, flag):
        if not flag:
            self.draw_lines.scatterPart.remove()
            self.draw_lines.scatterPart = None
        else:
            self.updatePointColor()
        self.canvas.draw()

    def showAxes(self, flag):
        self.draw_lines.ax1.get_xaxis().set_visible(flag)
        self.draw_lines.ax1.get_yaxis().set_visible(flag)
        self.canvas.draw()

    def updatePointColor(self):
        self.draw_lines.updateScatter(self.selectedFlagList)
        self.canvas.draw()

    # def dataChanged(self):
    #     self.dataChangedSignal.emit(self.data)

    # 改变点或者新增点, flag为0表示编辑点，flag为+1表示增加点, -1 表示删除点
    def updatePointPos(self, flag, data=None):
        # print("新增点", data)
        if data:
            if flag == 0:
                # 替换点坐标
                self.data[0][self.currentIndex], self.data[1][self.currentIndex] = data
                index = self.currentIndex
                self.setPlotArgs()
                self.tableUpdateSignal.emit({"flag": flag, "data": data, "index": index, "rows": None})

            elif flag == 1:
                index = self.currentIndex + 1 if True in self.selectedFlagList else self.dataLength
                self.currentIndex += 1
                self.data[0].insert(index, data[0])
                self.data[1].insert(index, data[1])
                self.dataLength += 1
                self.setPlotArgs()
                # print("进入table的点", data, index)
                self.tableUpdateSignal.emit({"flag": flag, "data": data, "index": index, "rows": None})
                # print("-=-=-=-=")
        elif flag == -1:
            # print("-----------delete---------------")
            index_list = [index for index in range(self.dataLength) if self.selectedFlagList[index]]
            x = [self.data[0][index] for index in range(self.dataLength) if index not in index_list]
            y = [self.data[1][index] for index in range(self.dataLength) if index not in index_list]
            self.currentIndex -= len(index_list)
            self.data = [x, y]
            self.setPlotArgs()
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

        self.show_point_chk = QCheckBox("显示点")
        self.show_point_chk.setCheckState(Qt.Checked)
        self.show_point_chk.setMaximumWidth(140)

        self.show_axes_chk = QCheckBox("显示坐标轴")
        self.show_axes_chk.setCheckState(Qt.Checked)
        self.show_point_chk.setCheckState(Qt.Checked)
        self.show_axes_chk.setCheckState(Qt.Checked)

        self.figureSettingLayout = QHBoxLayout()
        self.figureSettingLayout.addWidget(self.show_point_chk)
        self.figureSettingLayout.addWidget(self.show_axes_chk)

        self.verticalLayout_3.addWidget(self.main_tabWidget)
        self.verticalLayout_3.addLayout(self.figureSettingLayout)


        self.dockWidget.setFeatures(QDockWidget.AllDockWidgetFeatures)

        self.window.setMouseTracking(True)
        self.centralwidget.setMouseTracking(True)
        self.main_tabWidget.setMouseTracking(True)

        self.tabAddBtn = QPushButton()
        self.tabAddBtn.setIcon(getIcon(":resources//MyIcon//plus-circle-fill.svg"))
        self.tabAddBtn.setFlat(False)
        self.tabAddBtn.clicked.connect(lambda: self.addPage(False))

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
        self.setCanvasWidget(False)

        self.process_data.setData(self.data)
        self.action.triggered.connect(lambda: self.process_data.saveData())
        self.action_2.triggered.connect(lambda: self.process_data.exportData())
        self.process_data.getUpdateFunc([self.exportDataToTable, self.getTableData])

        self.action_3.triggered.connect(self.showSettings)

        self.process_data.exportDataSignal[list].connect(self.exportNewData)

    def exportNewData(self, data):
        self.statusbar.showMessage("表格数据导入中")
        self.exportDataToTable(data)
        self.statusbar.showMessage("表格数据导入完成！")
        self.data = data
        self.addPage(True)

    def showSettings(self):
        self.setMyDialog = SetMyDialog(self.currentCanvasWidget.draw_lines.settingsDict)
        self.setMyDialog.changeSettingSignal.connect(self.updateSettings)
        self.settingsDialog =  self.setMyDialog.dialog
        self.settingsDialog.show()

    def updateSettings(self, dict):
        # print(dict)
        self.currentCanvasWidget.draw_lines.settingsDict = dict
        self.currentCanvasWidget.draw_lines.updateCanvas(*self.data)

    def setCanvasWidget(self, isDataImport):
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
        self.show_point_chk.stateChanged[int].connect(self.showMaskPoint)
        self.show_axes_chk.stateChanged[int].connect(self.showAxes)
        self.currentCanvasWidget.doubleClicked[bool].connect(self.isShowInput)

        if not isDataImport:
            self.data = self.currentCanvasWidget.getData()
            print(self.data)
            self.exportDataToTable(self.data)

        self.process_data.setFig(self.currentCanvasWidget.getFigure())
        self.currentCanvasWidget.showCanvas(self.data)

    def showAxes(self, state):
        flag = True if state == 2 else False
        print("yes")
        self.currentCanvasWidget.showAxes(flag)

    def isShowInput(self, flag):
        if flag:
            self.showPosInput(0)
        else:
            self.showPosInput(1)

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
            # print("========show pos=========")
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
        if self.main_tabWidget.currentIndex() == -1:
            self.tableWidget.clearContents()
            self.tableWidget.setVisible(False)
            print(self.main_tabWidget.count())

    def setCurrentItem(self, row, col):
        self.editItemFlag = True
        self.currentItemText = self.tableWidget.item(row, col).text()

    def checkTableInput(self, row, col):
        try:
            # print("新增行{} 列{}".format(row, col))
            # 如果是由表格的右键菜单引起的项目内容变化，不检查其值
            # print(self.tableWidget.item(row, col).text())
            if self.editItemFlag:
                temp = float(self.tableWidget.item(row, col).text())
                self.data = self.getTableData()
                self.currentCanvasWidget.showCanvas(self.data)
            self.editItemFlag = False
        except Exception as ex:
            # print("这里有问题", ex)
            response_btn = QMessageBox.warning(self.tableWidget, "输入错误", "请输入一个小数！", QMessageBox.Yes)
            self.tableWidget.item(row, col).setText(self.currentItemText)

    def exportDataToTable(self, data=[]):
        self.tableWidget.setVisible(True)
        # print(len(data))
        if len(data[0]) == 0:
            QMessageBox.information(self.window, "导入数据为空","数据为空", QMessageBox.Ok)
            return False
        rows, cols = len(data[0]), len(data)
        # print("导入数据时的大小", rows, cols)
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(cols)
        for row in range(rows):
            for col in range(cols):
                item = QTableWidgetItem()
                item.setText(str(data[col][row]))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(row, col, item)
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
            self.tableWidget.insertRow(index)
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

    def addPage(self, flag):
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
        self.show_point_chk.stateChanged[int].disconnect(self.showMaskPoint)
        self.show_axes_chk.stateChanged[int].disconnect(self.showAxes)
        self.currentCanvasWidget.doubleClicked[bool].disconnect(self.isShowInput)


        self.currentCanvasWidget = canvasWidget
        self.currentCanvasWidget.getFigure().clf()
        self.setCanvasWidget(flag)
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
            self.show_point_chk.stateChanged[int].disconnect(self.showMaskPoint)
            self.show_axes_chk.stateChanged[int].disconnect(self.showAxes)
            self.currentCanvasWidget.doubleClicked[bool].disconnect(self.isShowInput)

            self.currentCanvasWidget = self.canvasWidgetList[index]
            self.setCanvasWidget(False)
        self.autoSwitchFlag = False


# 运行程序
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyWindow()
    ui_window = Ui_MyWindow(main_window)
    main_window.show()
    app.exec()




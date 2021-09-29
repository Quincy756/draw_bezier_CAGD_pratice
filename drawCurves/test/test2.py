from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)  # 用户界面后端渲染，用来以绘图的形式输出
from PyQt5.QtWidgets import QVBoxLayout
from matplotlib.figure import Figure  # 图表类
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy
import sys


class QmyFigureCanvas(QWidget):
    mouseMove = QtCore.pyqtSignal(numpy.float64, mpl.lines.Line2D)  # 自定义触发信号，用于与UI交互

    # mousePress = QtCore.pyqtSignal(numpy.float64,numpy.float64)
    # mouseRelease = QtCore.pyqtSignal(numpy.float64,numpy.float64)
    def __init__(self, parent=None, toolbarVisible=True, showHint=False):
        super().__init__(parent)
        # self.figure = mpl.figure.Figure()#公共属性figure
        self.figure = Figure()  # 公共属性figur
        figCanvas = FigureCanvas(self.figure)  # 创建FigureCanvas对象
        self.naviBar = NavigationToolbar(figCanvas, self)  # 创建工具栏

        actList = self.naviBar.actions()
        count = len(actList)
        self.__lastActtionHint = actList[count - 1]
        self.__showHint = showHint  # 是否显示坐标提示
        self.__lastActtionHint.setVisible(self.__showHint)
        self.__showToolbar = toolbarVisible  # 是否显示工具栏
        self.naviBar.setVisible(self.__showToolbar)

        layout = QVBoxLayout(self)
        layout.addWidget(self.naviBar)  # 添加工具栏
        layout.addWidget(figCanvas)  # 添加FigureCanvas对象
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.__cid = figCanvas.mpl_connect("scroll_event", self.do_scrollZoom)  # 支持鼠标滚轮缩放
        self.__cid1 = figCanvas.mpl_connect("pick_event", self.do_series_pick)  # 支持曲线抓取
        # self.__cid2 = figCanvas.mpl_connect("button_press_event",self.do_pressMouse)#支持鼠标按下
        self.__cid3 = figCanvas.mpl_connect("button_release_event", self.do_releaseMouse)  # 支持鼠标释放
        self.__cid4 = figCanvas.mpl_connect("motion_notify_event", self.do_moveMouse)  # 支持鼠标移动
        self.mouseIsPress = False
        self.pickStatus = False
        self.setDataHintVisible(True)


    # 公共函数接口
    def setToolbarVisible(self, isVisible=True):  # 是否显示工具栏
        self.__showToolbar = isVisible
        self.naviBar.setVisible(isVisible)

    def setDataHintVisible(self, isVisible=True):  # 是否显示坐标提示
        self.__showHint = isVisible
        self.__lastActtionHint.setVisible(isVisible)

    def redraw(self):  # 重绘曲线，快速调用
        self.figure.canvas.draw()

    def do_scrollZoom(self, event):  # 通过鼠标滚轮缩放
        ax = event.inaxes  # 产生事件axes对象
        if ax == None:
            return
        self.naviBar.push_current()
        xmin, xmax = ax.get_xbound()
        xlen = xmax - xmin
        ymin, ymax = ax.get_ybound()
        ylen = ymax - ymin

        xchg = event.step * xlen / 20
        xmin = xmin + xchg
        xmax = xmax - xchg
        ychg = event.step * ylen / 20
        ymin = ymin + ychg
        ymax = ymax - ychg
        ax.set_xbound(xmin, xmax)
        ax.set_ybound(ymin, ymax)
        event.canvas.draw()

    def do_series_pick(self, event):  # picker事件获取抓取曲线
        self.series = event.artist
        # index = event.ind[0]
        # print("series",event.ind)
        if isinstance(self.series, mpl.lines.Line2D):
            self.pickStatus = True

    def do_releaseMouse(self, event):  # 鼠标释放，释放抓取曲线
        if event.inaxes == None:
            return
        if self.pickStatus == True:
            self.series.set_color(color="black")
            self.figure.canvas.draw()
            self.pickStatus = False
        # self.mouseRelease.emit(event.xdata,event.ydata)

    def do_moveMouse(self, event):  # 鼠标移动，重绘抓取曲线
        print(event, event.xdata, event.ydata, "2")
        if event.inaxes == None:
            return
        if self.pickStatus == True:
            self.series.set_xdata([event.xdata, event.xdata])
            self.series.set_color(color="red")
            self.figure.canvas.draw()
            self.mouseMove.emit(event.xdata, self.series)  # 自定义触发信号，用于与UI交互

# 运行程序
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QmyFigureCanvas()
    main_window.show()
    app.exec()


import time

import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
from PyQt5.QtCore import pyqtSignal, QObject
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib as mpl
# 计算排列组合数
from scipy.special import comb, perm
# from drawCurves.test.test2 import QmyFigureCanvas
from matplotlib.animation import FuncAnimation
# import matplotlib.animation as ani


# 自定义画布
class MyFigureCanvas(FigureCanvas):
    mouseMove = pyqtSignal(np.float64, mpl.lines.Line2D)  # 自定义触发信号，用于与UI交互

    def __init__(self, *args, **kwargs):
        super(FigureCanvas, self).__init__(*args, **kwargs)
        self.mpl_connect("button_press_event", self.save_selectPos)  # 支持鼠标移动
        self.drawFunc = None

    def save_selectPos(self, event):
        if self.drawFunc:
            self.drawFunc()

    def getDrawFunc(self, drawFunc):
        self.drawFunc = drawFunc


# 自定义画图逻辑及样式
class DrawLines(QObject):

    updatePlotArgs = pyqtSignal(dict)

    def __init__(self):
        super(QObject, self).__init__()
        self.x = []
        self.y = []
        self.ax1 = None
        self.linePart = None
        self.scatterPart = None
        self.bezierCurve = None

        self.plotArgsDict = {}
        self.settingsDict = {
                             "point": {},
                             "line": {},
                             "bezier": {},
                             "axes": {
                                      "autoScale": True,
                                      "title": "",
                                      "x_min": 0,
                                      "x_max": 10,
                                      "y_min": 0,
                                      "y_max": 10,
                                      "x_tick": 1,
                                      "y_tick": 1
                                      },
                             "font": {"size": 2,
                                      "family": "宋体",
                                      "color": None}
                             }

        self.settingsDict["point"] = {"color": "#182C61",
                          "style": ".",
                          "size": 4
                          }


        self.settingsDict["bezier"] = {
                           "color": "#55E6C1",
                           "style": "-",
                           "width": 1,
                           }
        self.settingsDict["line"] = {"color": "#82589F",
                         "style": "-",
                         "width": "1"
                         }
        self.legend = None
        self.dataLength = 0
        self.figure = plt.figure(frameon=True, num="10")
        # 几个QWidgets
        self.canvas = MyFigureCanvas(self.figure)

        self.coefficientDict = {}
        for n in range(2, 20):
            self.getCoefficient(n)

        # 设置插值点
        self.coefficient = []
        self.t_array = np.arange(0, 1.001, 0.001)
        self.pos_num = len(self.t_array)

    def getCanvas(self):
        return self.canvas

    def getFigure(self):
        return self.figure

    def setPlotArgs(self, kwargs={}):
        self.plotArgsDict = dict(self.plotArgsDict, **kwargs)

    def getPlotArgs(self):
        return self.plotArgsDict

    def draw(self, x, y):
        # print("======================")
        # 线性插值
        # 贝塞尔插值
        self.bezier_x, self.bezier_y = self.bezierFunc(x, y)
        # print("---------插值完成-------------")
        self.x, self.y = x, y

        self.setPlotArgs()
        self.dataLength = len(self.x)
        self.color_list = ['r'] * self.dataLength

        # 新建区域ax1
        # figure的百分比,从figure 10%的位置开始绘制, 宽高是figure的80%
        left, bottom, width, height = 0.05, 0.05, 0.94, 0.94
        if self.ax1 and self.figure:
            self.ax1.cla()
            self.figure.clf()
            # self.canvas.draw()

        # 获得绘制的句柄
        self.ax1 = self.figure.add_axes([left, bottom, width, height])
        # self.ax1.set_axis_off()
        self.updateCanvas(self.x, self.y)


    def updateCanvas(self, x, y):
        # print(self.settingsDict)
        self.x, self.y = x, y
        # self.setPlotArgs()
        if self.settingsDict["axes"]["autoScale"]:
            ax = self.plotArgsDict["axes1"]
            self.ax1.set_xticks(ax["tick"][0])
            self.ax1.set_xlim(ax["lim"][0])
            self.ax1.set_yticks(ax["tick"][1])
            self.ax1.set_ylim(ax["lim"][1])
        else:
            print(self.settingsDict["axes"])
            ax = self.settingsDict["axes"]
            x_tick = np.arange(float(ax["x_min"]), float(ax["x_max"])+float(ax["x_tick"]) ,float(ax["x_tick"]))
            print(x_tick)
            self.ax1.set_xticks(x_tick)
            self.ax1.set_xlim(xmin=float(ax["x_min"]), xmax=float(ax["x_max"]))
            y_tick = np.arange(float(ax["y_min"]), float(ax["y_max"]) + float(ax["y_tick"]), float(ax["y_tick"]))
            self.ax1.set_yticks(y_tick)
            self.ax1.set_ylim(ymin=float(ax["y_min"]), ymax=float(ax["y_max"]))
            print(y_tick)
            print('------')
        print("yes", "==========")
        self.updateLinePart(self.x, self.y)
        self.updateBezierCurve(self.x, self.y)
        selectedFlagList = [False] * len(self.x)
        self.updateScatter(selectedFlagList)
        self.canvas.draw()

    def updateLinePart(self, x, y):
        self.x, self.y = x, y
        if self.linePart:
            for i, line in enumerate(self.linePart):
                self.linePart.pop(i)
                line.remove()
        print(len(self.settingsDict["line"]["style"]))
        self.linePart = self.ax1.plot(self.x, self.y,
                                      linestyle=self.settingsDict["line"]["style"],
                                      color=self.settingsDict["line"]["color"],
                                      linewidth=self.settingsDict["line"]["width"])

    def updateBezierCurve(self, x, y):
        self.bezier_x, self.bezier_y = self.bezierFunc(x, y)
        if self.bezierCurve:
            for i, line in enumerate(self.bezierCurve):
                self.bezierCurve.pop(i)
                line.remove()
        self.bezierCurve = self.ax1.plot(self.bezier_x, self.bezier_y,
                                         linestyle=self.settingsDict["bezier"]["style"],
                                         color=self.settingsDict["bezier"]["color"],
                                         linewidth=self.settingsDict["bezier"]["width"])


    def updateScatter(self, selectedFlagList=[]):
        self.dataLength = len(selectedFlagList)
        self.color_list = [self.settingsDict["point"]["color"]] * self.dataLength
        # print("----------color_list-----------", self.color_list)
        for i in range(self.dataLength):
            if selectedFlagList[i]:
                self.color_list[i] = 'b'
        try:
            if self.scatterPart:
                self.scatterPart.remove()
            self.scatterPart = self.ax1.scatter(self.x, self.y,
                                                marker=self.settingsDict["point"]["style"],
                                                s=self.settingsDict["point"]["size"]*10,
                                                color=self.color_list)
            # del self.scatterPart
        except Exception as ex:
            print(ex)

    # 获取系数矩阵
    def getCoefficient(self, n):
        if n in self.coefficientDict:
            coefficient = self.coefficientDict[n]
        else:
            coefficient = np.zeros(n + 1, np.int32)
            for i in range(n + 1):
                # 计算系数矩阵
                coefficient[i] = comb(n, i)
            self.coefficientDict[n] = coefficient
        return coefficient

    # 贝塞尔插值算法
    def bezierFunc(self, x, y):
        # print("-----------开始插值---------------")
        # start = time.time()


        ''' 普通公式算法
        b_xList = []
        b_yList = []
        点的个数要比阶数大1
        point_num = len(self.x)
        阶数
        n = point_num - 1
        for t in t_array:
            x_temp = 0.0
            y_temp = 0.0
            for i in range(n+1):
                # 计算系数
                coefficient = comb(n, i)
                x_temp += coefficient * self.x[i] * ((1.0-t)**(n-i)) * (t**i)
                y_temp += coefficient * self.y[i] * ((1.0-t)**(n-i)) * (t**i)
            b_xList.append(x_temp)
            b_yList.append(y_temp)
        return b_xList, b_yList
        '''

        # print("---------------")
        # 矩阵算法
        n = len(x) - 1
        # print(n, len(self.x) - 1)
        # print("data shape is {}".format(data.shape))
        # 如果点个数与上一次相同不重复计算 S*T矩阵
        if n != self.dataLength - 1:
            self.coefficient = self.getCoefficient(n)
            # print("-----------获取系数矩阵---------------")

            S = np.zeros((n+1, self.pos_num), dtype=np.float32)
            T = np.zeros((n+1, self.pos_num), dtype=np.float32)

            for i in range(n+1):
                S[i, :] = np.power((1-self.t_array), n-i)
                T[i, :] = np.power(self.t_array, i)
            self.st = S * T
            # print("-----------新建完成---------------")
        # print('-=-=')
        # print("S shape is, T shape is ， st shape is {}".format(self.st.shape))
        P_x = np.tile(x, (self.pos_num, 1)).T
        P_y = np.tile(y, (self.pos_num, 1)).T
        # print("P_x shape is {}, P_y shape is {}".format(P_x.shape, P_y.shape))
        M_x = P_x * self.st
        M_y = P_y * self.st
        # print("M_x shape is {}, M_y shape is {}".format(M_x.shape, M_y.shape))
        # 从缓存中读取数据
        B_x = np.dot(self.coefficient, M_x)
        B_y = np.dot(self.coefficient, M_y)
        # print("B_x shape is {}, B_y shape is {}".format(B_x.shape, B_y.shape))
        # print("------------------该算法计算共花费--------------------")
        # print(time.time()-start)
        return B_x.tolist(), B_y.tolist()

    def __str__(self):
        res = ""
        return res





















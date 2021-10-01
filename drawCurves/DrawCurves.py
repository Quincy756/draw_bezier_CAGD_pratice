import time

import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
from PyQt5.QtCore import pyqtSignal
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
class DrawLines:
    def __init__(self):
        self.x = []
        self.y = []
        self.ax1 = None

        self.dataLength = 0
        self.figure = plt.figure(frameon=True, num="10")
        # 几个QWidgets
        self.canvas = MyFigureCanvas(self.figure)

        self.coefficientDict = {}
        for n in range(2, 20):
            self.getCoefficient(n)

        # 设置插值点
        self.coefficient = []
        self.t_array = np.arange(0, 1.01, 0.02)
        self.pos_num = len(self.t_array)

    def setDrawStyles(self):
        pass

    def setFigure(self):
        pass

    def setCanvas(self):
        pass

    def getCanvas(self):
        return self.canvas

    def getFigure(self):
        return self.figure

    def draw(self, x, y):
        print("======================")
        print(self.dataLength)
        print(self.x, self.y)
        print(x, y)
        # 线性插值
        # self.x = [1, 2, 6, 20, 30]
        # self.y = [2, 20, 32, 35, 40]
        self.colorList = ['r', 'r','r', 'b']
        # 贝塞尔插值
        self.bezier_x, self.bezier_y = self.bezierFunc(x, y)
        print("---------插值完成-------------")
        self.x, self.y = x, y
        self.dataLength = len(self.x)
        min_x, max_x = min(self.x), max(self.x)
        min_y, max_y = min(self.y), max(self.y)

        start = time.time()
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
        self.ax1.set_xticks(np.arange(min_x-10, max_x+10, 5))
        self.ax1.set_xlim([min_x-10, max_x+10])
        self.ax1.set_yticks(np.arange(min_x-10, max_x+10, 5))
        self.ax1.set_ylim([min_y-10, max_y+10])
        self.ax1.set_title('area1')
        self.ax1.plot(self.x, self.y, "r-o", label="Curve 1")
        self.ax1.plot(self.bezier_x, self.bezier_y, "c-", label="Curve 2")
        # print("------------------除算法外共花费时间--------------------")
        # print(time.time() - start)
        self.figure.legend()
        self.canvas.draw()

    def getCoefficient(self, n):
        print("1")
        if n in self.coefficientDict:
            coefficient = self.coefficientDict[n]
            print("2")
        else:
            print("3")
            coefficient = np.zeros(n + 1, np.int32)
            for i in range(n + 1):
                # 计算系数矩阵
                coefficient[i] = comb(n, i)
            self.coefficientDict[n] = coefficient
        return coefficient

    def bezierFunc(self, x, y):
        print("-----------开始插值---------------")
        start = time.time()
        # 普通公式算法
        '''
        # b_xList = []
        # b_yList = []
        # 点的个数要比阶数大1
        # point_num = len(self.x)
        # 阶数
        # n = point_num - 1
        # for t in t_array:
        #     x_temp = 0.0
        #     y_temp = 0.0
        #     for i in range(n+1):
        #         # 计算系数
        #         coefficient = comb(n, i)
        #         x_temp += coefficient * self.x[i] * ((1.0-t)**(n-i)) * (t**i)
        #         y_temp += coefficient * self.y[i] * ((1.0-t)**(n-i)) * (t**i)
        #     b_xList.append(x_temp)
        #     b_yList.append(y_temp)
        # return b_xList, b_yList
        '''
        print("---------------")
        print(x, y)
        print(self.x, self.y)
        # 矩阵算法
        n = len(x) - 1
        print(n, len(self.x) - 1)
        # print("data shape is {}".format(data.shape))
        # 如果点个数与上一次相同不重复计算 S*T矩阵
        if n != self.dataLength - 1:
            self.coefficient = self.getCoefficient(n)
            print("-----------获取系数矩阵---------------")

            S = np.zeros((n+1, self.pos_num), dtype=np.float32)
            T = np.zeros((n+1, self.pos_num), dtype=np.float32)

            for i in range(n+1):
                S[i, :] = np.power((1-self.t_array), n-i)
                T[i, :] = np.power(self.t_array, i)
            self.st = S * T
            print("-----------新建完成---------------")
        print('-=-=')
        print("S shape is, T shape is ， st shape is {}".format(self.st.shape))
        P_x = np.tile(x, (self.pos_num, 1)).T
        P_y = np.tile(y, (self.pos_num, 1)).T
        print("P_x shape is {}, P_y shape is {}".format(P_x.shape, P_y.shape))
        M_x = P_x * self.st
        M_y = P_y * self.st
        print("M_x shape is {}, M_y shape is {}".format(M_x.shape, M_y.shape))
        # 从缓存中读取数据
        B_x = np.dot(self.coefficient, M_x)
        B_y = np.dot(self.coefficient, M_y)
        print("B_x shape is {}, B_y shape is {}".format(B_x.shape, B_y.shape))
        print("------------------该算法计算共花费--------------------")
        print(time.time()-start)
        return B_x.tolist(), B_y.tolist()

        #
        # # 复制行
        # coefficient = np.tile(coefficient, (2, n + 1))
        # # res = np.dot(coefficient, data)
        # res_array = np.zeros(n+1, dtype=np.float32)
        # # t_1 = np.power(1-t_array, n-i)
        # # t_2 = np.power(t, i)
        # for i in range(n+1):
        #     coefficient = np.array(comb(n, i))
        #     res_array[i] = coefficient * data

        #
        #
        # for t in t_array:
        #     x_temp = 0.0
        #     y_temp = 0.0
        #     for i in range(n+1):
        #         # 计算系数
        #         coefficient = comb(n, i)
        #         x_temp += coefficient * self.x[i] * ((1.0-t)**(n-i)) * (t**i)
        #         y_temp += coefficient * self.y[i] * ((1.0-t)**(n-i)) * (t**i)
        #     b_xList.append(x_temp)
        #     b_yList.append(y_temp)
        # return b_xList, b_yList


# 定义插值算法类
class InterpolAlgo:
    def __init__(self, pointSet):
        pass

# 定义
class BezierCurve(InterpolAlgo):

    def __init__(self, pointSet=None):
        super(InterpolAlgo, self).__init__(pointSet)
        self.pointSet = pointSet
        self.result = []

    def get_result(self):
        return self.result

    def set_pointSet(self, pointSet):
        self.pointSet += pointSet

















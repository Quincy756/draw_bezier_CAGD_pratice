import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class DrawLines:
    def __init__(self):
        # 几个QWidgets
        self.figure = plt.figure(facecolor='#FFD7C4')  # 可选参数,facecolor为背景颜色
        self.canvas = FigureCanvas(self.figure)

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

    def draw(self, func):
        func()
















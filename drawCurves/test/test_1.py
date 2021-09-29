# 0.导入需要的包和模块
from PyQt5.Qt import *
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Major")
        self.resize(500, 500)
        self.setMouseTracking(True)
        self.label = QLabel(self)
        self.label.resize(200,200)
        self.label.setText("测试")
        self.label.setStyleSheet("background-color:blue;")
        self.label.setMouseTracking(True)


    def mouseMoveEvent(self,event):
        x = event.x()
        y = event.y()
        text = "x:{0},y:{1}".format(x,y)
        self.label.setText(text)
        print(text)

if __name__ == '__main__':

    # 1.创建一个应用程序对象
    app = QApplication(sys.argv)
    # 2.控件的操作
    # 2.1创建控件
    window = Window()
    # 2.2设置控件



    # 2.3展示控件
    window.show()
    # 3.应用程序的执行，进入到信息循环
    sys.exit(app.exec_())


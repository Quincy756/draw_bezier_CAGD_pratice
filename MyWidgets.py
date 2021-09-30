from PyQt5.QtWidgets import QMenu, QAction, QFileDialog
from Data.processExcel import *



class MyFileMenu(QMenu):
    def __init__(self):
        QMenu.__init__(self, "文件")
        self.saveAction = QAction("保存")
        self.importAction = QAction("导入")
        self.exitAction = QAction("退出")
        actions_list = [self.saveAction, self.importAction]
        self.addActions(actions_list)
        # 添加分割线
        self.addSeparator()
        self.addAction(self.exitAction)

    def activateMenu(self, data):
        data = processData(data)
        self.saveAction.triggered.connect(data.saveData)
        self.importAction.triggered.connect(data.importData)

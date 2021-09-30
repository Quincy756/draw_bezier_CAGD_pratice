from PyQt5.QtWidgets import  *


class processData:
    def __init__(self, data=None):
        self.data = data

    def saveData(self):
        print("yes")
        self.saveDataPath = "..//data//My Data/新建文件.xlsx"
        self.saveDataPath = "Data/"
        filedialog = QFileDialog()
        filedialog.setFileMode(QFileDialog.Directory)
        file_path, file_name = QFileDialog.getSaveFileName(filedialog, "保存", self.saveDataPath, "*.xlsx")
        if file_path:
            print(file_path)
            pass

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data

    def importData(self):
        # self.importDataPath = "..//data//我的数据/"
        self.importPath = "/Data/"
        filedialog = QFileDialog()
        filedialog.setFileMode(QFileDialog.ExistingFiles)
        file_path, file_name = QFileDialog.getOpenFileName(filedialog, "导入", self.importPath, "*.xlsx")
        if file_path:
            print(file_path)
            pass


# if __name__ == "__main__":
#     test = processData()
#     test.saveData()





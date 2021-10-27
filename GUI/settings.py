# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(596, 653)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 571, 621))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.stackedWidget = QtWidgets.QStackedWidget(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.page_5)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 541, 571))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(self.verticalLayoutWidget_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox_3)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 174, 151))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setVerticalSpacing(12)
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setMinimumSize(QtCore.QSize(0, 25))
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.spinBox_3 = QtWidgets.QSpinBox(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_3.sizePolicy().hasHeightForWidth())
        self.spinBox_3.setSizePolicy(sizePolicy)
        self.spinBox_3.setMinimumSize(QtCore.QSize(0, 25))
        self.spinBox_3.setObjectName("spinBox_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBox_3)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.set_lineColor_btn = QtWidgets.QPushButton(self.formLayoutWidget)
        self.set_lineColor_btn.setMinimumSize(QtCore.QSize(30, 30))
        self.set_lineColor_btn.setMaximumSize(QtCore.QSize(30, 30))
        self.set_lineColor_btn.setStyleSheet("background-color: rgba(0, 255, 0, 255);")
        self.set_lineColor_btn.setText("")
        self.set_lineColor_btn.setObjectName("set_lineColor_btn")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.set_lineColor_btn)
        self.comboBox_2 = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_2)
        self.label_8 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_8.setMinimumSize(QtCore.QSize(0, 25))
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.horizontalLayout_4.addWidget(self.groupBox_3)
        self.groupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget_2)
        self.groupBox.setObjectName("groupBox")
        self.formLayoutWidget_3 = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(60, 20, 123, 141))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setVerticalSpacing(12)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_10 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_10.setMinimumSize(QtCore.QSize(0, 25))
        self.label_10.setObjectName("label_10")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.spinBox_4 = QtWidgets.QSpinBox(self.formLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_4.sizePolicy().hasHeightForWidth())
        self.spinBox_4.setSizePolicy(sizePolicy)
        self.spinBox_4.setMinimumSize(QtCore.QSize(0, 25))
        self.spinBox_4.setObjectName("spinBox_4")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox_4)
        self.label_11 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_11.setObjectName("label_11")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.set_pointColor_btn = QtWidgets.QPushButton(self.formLayoutWidget_3)
        self.set_pointColor_btn.setMinimumSize(QtCore.QSize(30, 30))
        self.set_pointColor_btn.setMaximumSize(QtCore.QSize(30, 30))
        self.set_pointColor_btn.setStyleSheet("background-color: rgba(0, 255, 0, 255);")
        self.set_pointColor_btn.setText("")
        self.set_pointColor_btn.setObjectName("set_pointColor_btn")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.set_pointColor_btn)
        self.label_12 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_12.setObjectName("label_12")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.comboBox_3 = QtWidgets.QComboBox(self.formLayoutWidget_3)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.comboBox_3)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.groupBox_2 = QtWidgets.QGroupBox(self.verticalLayoutWidget_2)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 201, 121))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setHorizontalSpacing(8)
        self.formLayout_2.setVerticalSpacing(12)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_7 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_7.setMinimumSize(QtCore.QSize(0, 25))
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit.setMinimumSize(QtCore.QSize(60, 25))
        self.lineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_14 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_14.setMinimumSize(QtCore.QSize(0, 25))
        self.label_14.setObjectName("label_14")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.spinBox_5 = QtWidgets.QSpinBox(self.formLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_5.sizePolicy().hasHeightForWidth())
        self.spinBox_5.setSizePolicy(sizePolicy)
        self.spinBox_5.setMinimumSize(QtCore.QSize(60, 25))
        self.spinBox_5.setMaximumSize(QtCore.QSize(120, 16777215))
        self.spinBox_5.setObjectName("spinBox_5")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBox_5)
        self.label_15 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_15.setObjectName("label_15")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.pushButton_7 = QtWidgets.QPushButton(self.formLayoutWidget_2)
        self.pushButton_7.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_7.setText("")
        self.pushButton_7.setFlat(False)
        self.pushButton_7.setObjectName("pushButton_7")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.pushButton_7)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox_4 = QtWidgets.QGroupBox(self.verticalLayoutWidget_2)
        self.groupBox_4.setObjectName("groupBox_4")
        self.formLayoutWidget_5 = QtWidgets.QWidget(self.groupBox_4)
        self.formLayoutWidget_5.setGeometry(QtCore.QRect(280, 30, 231, 132))
        self.formLayoutWidget_5.setObjectName("formLayoutWidget_5")
        self.formLayout_5 = QtWidgets.QFormLayout(self.formLayoutWidget_5)
        self.formLayout_5.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_5.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout_5.setContentsMargins(0, 0, 0, 0)
        self.formLayout_5.setHorizontalSpacing(7)
        self.formLayout_5.setVerticalSpacing(12)
        self.formLayout_5.setObjectName("formLayout_5")
        self.Label_2 = QtWidgets.QLabel(self.formLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_2.sizePolicy().hasHeightForWidth())
        self.Label_2.setSizePolicy(sizePolicy)
        self.Label_2.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Label_2.setObjectName("Label_2")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label_2)
        self.yLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yLineEdit.sizePolicy().hasHeightForWidth())
        self.yLineEdit.setSizePolicy(sizePolicy)
        self.yLineEdit.setMinimumSize(QtCore.QSize(40, 25))
        self.yLineEdit.setMaximumSize(QtCore.QSize(80, 40))
        self.yLineEdit.setObjectName("yLineEdit")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.yLineEdit)
        self.horizontalSlider = QtWidgets.QSlider(self.formLayoutWidget_5)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.horizontalSlider)
        self.yLabel = QtWidgets.QLabel(self.formLayoutWidget_5)
        self.yLabel.setObjectName("yLabel")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.yLabel)
        self.yLineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget_5)
        self.yLineEdit_2.setMinimumSize(QtCore.QSize(0, 25))
        self.yLineEdit_2.setMaximumSize(QtCore.QSize(80, 40))
        self.yLineEdit_2.setObjectName("yLineEdit_2")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.yLineEdit_2)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.formLayoutWidget_5)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.horizontalSlider_2)
        self.line_3 = QtWidgets.QFrame(self.groupBox_4)
        self.line_3.setGeometry(QtCore.QRect(240, 20, 20, 161))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox_4)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 70, 231, 79))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_13.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_4.setMaximumSize(QtCore.QSize(70, 16777215))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_5.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_5.setMaximumSize(QtCore.QSize(70, 16777215))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout.addWidget(self.lineEdit_5, 1, 3, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(70, 16777215))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 0, 1, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(70, 16777215))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 0, 3, 1, 1)
        self.formLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_4)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(10, 30, 89, 21))
        self.formLayoutWidget_4.setObjectName("formLayoutWidget_4")
        self.formLayout_4 = QtWidgets.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.formLayout_4.setObjectName("formLayout_4")
        self.Label = QtWidgets.QLabel(self.formLayoutWidget_4)
        self.Label.setObjectName("Label")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label)
        self.CheckBox = QtWidgets.QCheckBox(self.formLayoutWidget_4)
        self.CheckBox.setChecked(True)
        self.CheckBox.setObjectName("CheckBox")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.CheckBox)
        self.horizontalLayout_3.addWidget(self.groupBox_4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.stackedWidget.addWidget(self.page_5)
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.stackedWidget.addWidget(self.page_6)
        self.horizontalLayout.addWidget(self.stackedWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox_3.setTitle(_translate("Dialog", "线"))
        self.label_5.setText(_translate("Dialog", "线宽:"))
        self.label_4.setText(_translate("Dialog", "颜色: "))
        self.label_6.setText(_translate("Dialog", "样式:"))
        self.comboBox.setItemText(0, _translate("Dialog", "------"))
        self.comboBox.setItemText(1, _translate("Dialog", "......"))
        self.comboBox.setItemText(2, _translate("Dialog", "-.-.-."))
        self.comboBox_2.setItemText(0, _translate("Dialog", "连接线"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "贝塞尔曲线"))
        self.label_8.setText(_translate("Dialog", "选择曲线"))
        self.groupBox.setTitle(_translate("Dialog", "点"))
        self.label_10.setText(_translate("Dialog", "大小"))
        self.label_11.setText(_translate("Dialog", "颜色: "))
        self.label_12.setText(_translate("Dialog", "样式:"))
        self.comboBox_3.setItemText(0, _translate("Dialog", "."))
        self.comboBox_3.setItemText(1, _translate("Dialog", ","))
        self.comboBox_3.setItemText(2, _translate("Dialog", "o"))
        self.comboBox_3.setItemText(3, _translate("Dialog", "^"))
        self.comboBox_3.setItemText(4, _translate("Dialog", "v"))
        self.comboBox_3.setItemText(5, _translate("Dialog", "s"))
        self.comboBox_3.setItemText(6, _translate("Dialog", "D"))
        self.comboBox_3.setItemText(7, _translate("Dialog", "h"))
        self.groupBox_2.setTitle(_translate("Dialog", "绘图"))
        self.label_7.setText(_translate("Dialog", "标题:"))
        self.label_14.setText(_translate("Dialog", "字体大小:"))
        self.label_15.setText(_translate("Dialog", "字体颜色: "))
        self.groupBox_4.setTitle(_translate("Dialog", "坐标轴"))
        self.Label_2.setText(_translate("Dialog", "x轴刻度:"))
        self.yLabel.setText(_translate("Dialog", "y轴刻度:"))
        self.label_3.setText(_translate("Dialog", "x轴范围:"))
        self.label_13.setText(_translate("Dialog", "y轴范围:"))
        self.label_2.setText(_translate("Dialog", "-"))
        self.label.setText(_translate("Dialog", "-"))
        self.Label.setText(_translate("Dialog", "自动调整"))
        self.pushButton.setText(_translate("Dialog", "保存"))
        self.pushButton_2.setText(_translate("Dialog", "取消"))
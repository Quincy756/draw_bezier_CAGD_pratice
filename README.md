# 贝塞尔插值曲线绘制软件设计报告

## 系统设计

整个绘图软件基于n贝塞尔插值公式进行基础设计，在实现绘制n阶贝塞尔曲线的高效绘制算法的基础上加入了各种对曲线的操作操作，使之成为一个完整的曲线绘制软件。该项目主要使用python语言进行编写，**主要结合PyQt5、matplotlib、numpy和openxl等库**进行开发，整个项目的代码量在2500行左右。

系统设计主要包括界面设计、功能设计、程序设计这三部分。整个项目在github上进行开源，开源地址为: <https://github.com/Quincy756/draw_bezier_CAGD_pratice>。同时整个系统可扩展，可以在源程序的基础上扩展开发其他曲线如拉格朗日、B样条曲线等的绘制程序。

###  项目结构

系统的项目结构如图1所示。Data文件夹中包含了与数据导入导出相关的程序文

![image-20211124203310410](https://raw.githubusercontent.com/Quincy756/picutres/main/img/RVM/image-20211124203310410.png)

图1 系统的项目结构

件，dist和build文件夹以及main.spec文件为使用pyinstaller打包后生成的运行文件，其中dist文件夹中存有整个项目的exe文件，直接点击即可运行。

Pipfile和Pipfile.lock是建立程序运行环境所需的环境。src.py和src.qrc是用来导入所需的程序资源的文件。GUI则包含了界面设计的ui文件和相关的GUI界面程序。程序的参考文档为README.md，开发者可以根据该文档进行二次开发和扩展。drawCurves文件夹包含了绘制曲线的算法以及相应的绘图接口程序。

## 界面设计

使用Qt designer对软件进行了整体界面设计，软件的主界面主要由菜单栏、tab栏和包含在其中的绘图界面和数据展示界面等组成。绘图界面主要负责图形的绘制和与用户的绘图交互，数据展示界面主要负责通过表格动态的展示数据。此外，还设计了一个设置界面，该界面能够对用户绘制的图形的点、线的颜色样式和坐标轴等进行多种多样的设置，因为时间关系没有对界面进行进一步的美化操作。

### 主界面

主界面主要以menuBar、tabBar和statusBar基本框架，每一个tabBar中都嵌入了一个绘图区，不同的tab的绘图区域是相互不受干扰的，可以任意切换，如图2所示。绘图区由两个x、y坐标轴和相应的刻度组成。数据展示界面设计为一个表格界面，其嵌入到一个可停靠控件当中，可以将其拖拽与主界面进行分离和再次放入主界面的不同区域内。

![image-20211124203348078](https://raw.githubusercontent.com/Quincy756/picutres/main/img/RVM/image-20211124203348078.png)

图2 主界面

菜单栏menubar展示了主要的功能菜单，每个主功能菜单又加入了子菜单。状态栏statusbar设计用来显示系统的状态信息，点的操作信息等。

### 2.2 设置界面

设置界面如图3所示，主要分成了对线、点、绘图和坐标轴等部分。使用了多个不同种类的控件进行设计，有利于用户提交表单。同时针对每个设置功能进行了分组，使得界面不至于太过混乱。

![image-20211124203409922](https://raw.githubusercontent.com/Quincy756/picutres/main/img/RVM/image-20211124203409922.png)

图 3 设置界面

## 功能设计

### 插值点的相关功能

插值点的相关功能主要包括插值点的坐标显示、新建、选取、修改、删除、取消选点等功能。同时能够检查用户输入，如果输入不为数字就会报错。还能够拖拽点，拖拽点的时候曲线会随之改变，如果拖拽的点超出所在坐标轴后坐标轴会自动的修改，以保证曲线在绘图区域内显示。

(1) 点的坐标显示：通过窗口底部的状态栏可以实时显示鼠标所在位置的点的坐标，并且能够显示已选中的点，如图4所示。

![image-20211124203421664](https://raw.githubusercontent.com/Quincy756/picutres/main/img/RVM/image-20211124203421664.png)

图4 选中点后状态栏坐标

(2) 新建点与插入点：可以通过三种方式新建点：

-   直接选中任意空白区域新建点

-   在数据展示表格处鼠标右键弹出菜单选择增加点

-   在绘图区鼠标右键弹出菜单选择增加点

-   在选取点后进行增加点就会在选中点后插入新增的点

(3) 点的选取：鼠标左键能够选取任意个给定的插值点，能实现如下功能：

-   选取点后点的颜色会发生改变

-   选中点时鼠标的游标会变成十字型

-   状态栏会显示所选点的坐标

-   在任意在空白区域点击即可取消选点

(4) 点的修改：如图5所示，可以通过样式设置界面修改点的大小、样式、颜色等属性。可以通过以下几种方式修改点的具体坐标：

 ![image-20211124203434152](https://raw.githubusercontent.com/Quincy756/picutres/main/img/RVM/image-20211124203434152.png)

 图5 点的修改

-   双击要修改的点进行更改

-   选中点后鼠标右键选择编辑即可更改

-   在数据展示表格处选中点所在单元格，双击进行更改

(5) 点的删除：不仅可以删除点还可以批量删除点，可以通过以下几种方式删除点：

-   选中点后鼠标右键弹出菜单中选择删除点

-   在数据展示表格处选中点所在单元格，鼠标右键弹出菜单后选择删除点

### 绘图区域的相关功能

用户能够新建多个标签页(tab)，并能够保存标签页、删除标签页、切换标签页，每个tab之间的绘图区域是可以自由切换互不影响的，如图6所所示。每个标签页中还能够选择是否显示点和是否显示坐标轴，关闭标签页时会提醒用户是否保存。

![image-20211124204028086](https://raw.githubusercontent.com/Quincy756/picutres/main/img/RVM/image-20211124204028086.png)![image-20211124204033902](https://raw.githubusercontent.com/Quincy756/picutres/main/img/RVM/image-20211124204033902.png)        

图6 多个tab进行切换绘图

### 设置功能

设置界面有两种，如果勾选坐标轴自动调整那么如图7右所示。可以对x轴和y轴范围和刻度进行详细的设计。能够设置线的颜色、线宽、样式和点的大小、颜色、样式等。

![image-20211124204156919](https://raw.githubusercontent.com/Quincy756/picutres/main/img/RVM/image-20211124204156919.png)

图7 设置界面

![image-20211124204219962](https://raw.githubusercontent.com/Quincy756/picutres/main/img/RVM/image-20211124204219962.png)

如图8 (a)(b)(c)展示了通过设置不同的点线样式绘制的图形效果。

![image-20211124204231568](https://raw.githubusercontent.com/Quincy756/picutres/main/img/RVM/image-20211124204231568.png)

\(a\)

![image-20211124204237209](https://raw.githubusercontent.com/Quincy756/picutres/main/img/RVM/image-20211124204237209.png)

\(b\)

![image-20211124204243195](https://raw.githubusercontent.com/Quincy756/picutres/main/img/RVM/image-20211124204243195.png)

\(c\)

图8 不同样式设置的效果

### 数据和曲线的导入导出

能够对不同标签页的曲线进行导出，可以导出为excel表格，或者png图片。能够将excel表格中固定格式的数据点导入到数据展示表格中，并自动绘制曲线。如图9所示。

![image-20211124204256141](https://raw.githubusercontent.com/Quincy756/picutres/main/img/RVM/image-20211124204256141.png)

图 9 导出后的曲线图片

## 程序设计

整个程序分为以下主要一些类：

(1) Ui_MainWindow类，主要负责窗口主界面的创建，包括数据展示界面和绘图等界面

(2) Ui_MyWindow类，继承自Ui_MainWindow，同时加入了很多与主界面控件交互的函数，主要用于操作窗口主界面。

(3) CanvasContainer类，主要负责创建绘图区的画布和相应的与绘图区进行交互的操作函数。

(4) CanvasWidget类，主要负责实例化画布，并进行画布内事件的回调。

(5) InputPointWdt类，即可以编辑点的坐标的小窗口，负责收集用户填写的坐标数据，并返回给有需要的模块。

(6) Drawlines类，主要负责根据输入的点绘制指定样式、大小、颜色的曲线和点、坐标轴等，同时根据用户的鼠标交互进行实时绘制曲线。

(7) ExcelHandle类，主要负责处理数据从excel表格导入和导出为excel文件。

(8) ProcessData类，主要负责数据的处理，从用户需要的文件位置选择文件打开或者进行保存。

(9) Ui_Dialog类，主要负责展示设置界面，对组件的基本状态进行设置。

(10) SetMyDialog类，主要负责设置界面中的用户输入设置的数据交换，以及与控件与用户的交互功能。

按模块划分可分为GUI模块，用户交互模块、数据处理模块和绘制模块，具体的uml类图及方法如图10所示。

![CAGD copy](https://raw.githubusercontent.com/Quincy756/picutres/main/img/RVM/CAGD%20copy.png)

图 10 软件的UML类图

### GUI模块

GUI模块主要由Ui_MainWindow类、InputPointWdt类和Ui_Dialog类组成。对于每个类将简要介绍其主要函数及其功能。

Ui_MainWindow类有两个主要函数setupUi和retranslateUi，其中前一个负责主界面的初始化和布局，后一个负责主界面语言的国际化。

InputPointWdt类继承自Qwidget类，主要函数为setLineEditText和getData，setLineEditText函数主要是在双击时将lineEdit编辑框显示为点的坐标，getData函数能够获取用户输入的坐标并进行保存校验。

Ui_Dialog类和Ui_MainWindow一样，也有setupUi和retranslateUi函数，setupUi负责设置界面的初始化和布局选项，retranslateUi负责主界面语言的国际化。

### 用户交互模块

用户交互模块主要由Ui_MyWindow类和SetMyDialog类组成。这两个类分别继承自Ui_MainWindow类和Ui_Dialog类，但是与之不同的是，Ui_MyWindow类和SetMyDialog类主要创造了与用户交互的接口和外部程序可直接调用的接口，而Ui_MainWindow类和Ui_Dialog类仅仅只是展示界面，界面的功能接口没有具体实现。之所以要这样做是是实现逻辑与界面分离，这样可以改变界面而不需要变更逻辑部分，实现类间的解耦。

#### Ui_MyWindow类

Ui_MyWindow类的主要函数如下，除setupUi外可分为大致分为四类，如下所示：

-   setupUi(self, Window): 继承自Ui_MainWindow，实现主界面中各部分组件的初始化、状态设置、信号与槽函数的设置等。

(1) 数据表格相关

-   exportNewData(self, data): 导入新的数据，负责实现菜单栏中的导入选项，弹出文件选择对话框选择要导入的文件后调用exportDataToTable(self, data=\[\])。

-   exportDataToTable(self, data=\[\]): 将转换好的数据导入到界面的数据中。

-   changeTableData(self, flag): 根据输入flag改变表格数据。

-   getTableData(self): 获取主界面表格中的数据。

-   checkTableInput(self, row, col): 校验表格输入。

-   showTableMenu(self): 展示表格右键菜单。

(2) 标签页相关

-   setCanvasWidget(self, isDataImport): 负责设置当前的画布，如果切换标签页需要更换不同的画布。

-   addPage(self, flag): 创建新的标签页，并分配画布进行初始化。

-   setCurrentTab(self, index): 设置第index个标签页为当前标签页。

-   closeCurrentTab(self): 关闭当前标签页并提醒用户是否保存。

(3) 展示相关

-   showAxes(self, state): 根据输入的state确定是否显示坐标轴。

-   isShowInput(self, flag): 据输入的flag确定是否显示坐标编辑对话框。

-   showPosInput(self, flag): 负责双击时创建可以输入位置坐标的对话框。

-   showContextMenu(self, pos): 展示右键菜单。

-   showSettings(self): 负责实现菜单栏中的设置选项，并弹出设置对话框。

(4) 更新相关

-   updateSettings(self, dict): 更新设置对话框中的各组件设置。

-   updateData(self, data): 更新点的数据及画布。

-   updateSelectState(self, selectState): 更新所选点的状态

-   updatePointPos(self, flag): 更新点的坐标数据。

-   updateMyTable(self, kwargs): 更新数据表格。

#### SetMyDialog类

SetMyDialog类的主要函数如下：

-   setupUi(self, Window): 继承自Ui_Dialog，实现设置界面中各部分组件的初始化、状态设置、信号与槽函数的设置等。

-   setLines(self, index): 选择贝塞尔曲线或者直线进行设置。

-   updateValue(self): 坐标轴范围滑动时更新值。

-   updateAxesSetting(self): 更新坐标轴相关设置。

-   setAxesRange(self, text=\"\"): 设置坐标轴相关范围。

-   showAxesLineEdit(self, flag): 展示坐标轴编辑选项。

-   editAxesRange(self, state): 编辑坐标轴的范围。

-   updateXTick(self, value)、updateYTick(self, value): 更新坐标轴刻度值。

-   updateXSliderValue(self, text)、updateYSliderValue(self, text): 更新刻度滑动条的值和编辑栏内的数值。

-   updateSliderRange(self): 更新刻度滑动条的最大最小范围。

-   changeSettings(self): 保存时改变设置。

-   getSettings(self): 弹出设置对话框前先获取设置。

-   selectColor(self, btn, name): 弹出颜色选择对话框并选择颜色。

### 画图模块

画图模块由CanvasContainer类、Drawlines类和CanvasWidget类组成。其中，CanvasWidget类负责实例化一个画布，并将这个画布的句柄传给CanvasContainer类。由CanvasContainer类负责画布的对外接口和相关操作的实现。Drawlines类负责在画布中绘制具体的线、坐标轴的设置等。

#### CanvasContainer类

该类的主要函数和说明如下：

-   setPlotArgs(self, kwargs={}): 设置绘图的参数

-   showCanvas(self, data=None): 显示画布。

-   keyPress(self, event): 鼠标点击、双击事件触发的函数。

-   keyRelease(self, event): 鼠标松开事件触发的函数。

-   keyMove(self, event): 鼠标移动事件触发的函数。

-   getPointDistance(self, p1, p2): 获取两个点的距离，用于选取给定坐标的点。

-   showMaskPoint(self, flag): 展示点。

-   showAxes(self, flag): 展示坐标轴。

-   updatePointColor(self): 选中点后更新点的颜色

-   updatePointPos(self, flag, data=None): 更新点的坐标位置

-   resetPointState(self): 重新设置点的状态

-   getData(self): 返回当前画布的点的数据

-   setData(self, data): 设置当前画布的点的数据

#### Drawlines类

该类用于自定义画图逻辑和相关的样式，其主要函数如下：

-   getCanvas(self): 返回当前绘图的画布，即在哪个画布上绘图。

-   getFigure(self): 返回当前绘图的图像(figure)。

-   setPlotArgs(self, kwargs={}): 设置绘图所需的参数。

-   getPlotArgs(self): 返回绘图参数。

-   draw(self, x, y): 给定点的列表绘制相应的曲线。

-   updateCanvas(self, x, y): 更新绘图所需的画布。

-   updateLinePart(self, x, y): 更新绘图区域中的折线部分。

-   updateBezierCurve(self, x, y): 更新绘图区域中的贝塞尔曲线。

-   updateScatter(self, selectedFlagList=\[\]): 更新绘图。

-   getCoefficient(self, n): 返回n阶贝塞尔曲线的系数。

-   bezierFunc(self, x, y): 进行贝塞尔曲线插值。

其中bezierFunc(self, x, y)主要有以下两种写法：

第一种，直接用for循环进行多项式运算，效率极低。如下所示：

```
def bezierFunc(self, x, y):
    b_xList = []
    b_yList = []
    # 点的个数要比阶数大1
    point_num = len(x)
    # 阶数
    n = point_num - 1
    for t in t_array:
    x_temp = 0.0
    y_temp = 0.0
    for i in range(n+1):
    # 计算系数
    coefficient = comb(n, i)
    x_temp += coefficient * x[i] * ((1.0-t)**(n-i)) * (t**i)
    y_temp += coefficient * y[i] * ((1.0-t)**(n-i)) * (t**i)
    b_xList.append(x_temp)
    b_yList.append(y_temp)
return b_xList, b_yList
```

第二种，将多项式运算转换为矩阵运算。同时将多项式系数缓存到内存中，可直接进行调用，具体程序如下所示：
```
def  bezierFunc(self, x, y):
    b_xList = []
    b_yList = []
    # 点的个数要比阶数大1
    point_num = len(x)
    # 阶数
    n = point_num - 1
    for t in t_array:
    x_temp = 0.0
    y_temp = 0.0
    for i in range(n+1):
    # 计算系数
    coefficient = comb(n, i)
    x_temp += coefficient * x[i] * ((1.0-t)**(n-i)) * (t**i)
    y_temp += coefficient * y[i] * ((1.0-t)**(n-i)) * (t**i)
    b_xList.append(x_temp)
    b_yList.append(y_temp)
return b_xList, b_yList
```
### 4.3 数据处理模块

数据处理模块由ExcelHandle类和processData(QObject)类组成。其中ExcelHandle类主要负责将数据转换为excel表格和将excel表格数据转换为绘图所需要的数据。

ExcelHandle类的主要函数如下：

-   getData(self)：返回转换后的绘图数据格式。

-   setData(self, data)：获取需要进行转换的数据。

-   getWorkbook(self, file_path, sheetName=\"Sheet1\")：打开excel表格并获取表单。

-   saveData(self, file_path, sheetName=\"Sheet1\")：将绘图数据转换为excel表格数据存入excel表格中。

-   exportData(self, file_path, sheetName=\"Sheet1\")：打开excel表格并读取其数据，转换为绘图所需的数据。

processData类的主要函数如下：

-   saveData(self)：打开文件保存对话框，获取要导出的文件路径后保存数据为指定格式。

-   setFig(self, figure): 获取需要保存的图像。

-   saveFig(self, file_path): 将需要保存的图像保存到制定路径。

-   setData(self, data): 获取需要保存的数据。

-   getData(self): 返回导入的数据。

-   exportData(self): 打开文件选择对话框，获取要导入的文件路径后导入数据。

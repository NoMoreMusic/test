# -*- coding: utf-8 -*-
import sys
import os
import math
import wx
import pandas as pd
import sip
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout , QPushButton, QSizePolicy, QMainWindow, QListWidget, QListWidgetItem, QFileDialog, QHBoxLayout
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from MainWin1 import Ui_MainWindow

#初始化绘图
class MyMplCanvas(FigureCanvas):
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        
        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        self.fig = Figure(figsize=(width, height),dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        self.axes.clear()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        FigureCanvas.updateGeometry(self)

    def start_static_plot(self):
        self.fig.suptitle('测试静态图')  #注意此处为sup不是sub
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * math.pi * t)
        self.axes.plot(t, s)
        self.axes.set_ylabel('静态图: Y轴')
        self.axes.set_xlabel('静态图: X轴')
        self.axes.grid(True)
    
    def start_item_plot(self, item):
        # i = 1
        # plotPath = item[i]
        self.fig.suptitle("光谱图")
        for plotPath in item:
            print(f"File_name: {plotPath}")
            filename = os.path.basename(plotPath) 
            filename = filename.split('.')[0]   #获取不带后缀的路径文件名
            # self.fig.suptitle(f"光谱图: {filename}")  #注意此处为sup不是sub
            readData = pd.read_csv(plotPath)
            xdata = readData.iloc[:,0].tolist()
            ydata = readData.iloc[:,1].tolist()
            self.axes.plot(xdata, ydata)
            self.axes.set_ylabel('静态图: Y轴')
            self.axes.set_xlabel('静态图: X轴')
            self.axes.grid(True)
    


        

class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.filePath = ""  #类变量初始化
        self.mpl = MyMplCanvas(self, width=5, height=4, dpi=100)
        self.setupUi(self)
        self.initUi()   #初始化绘图界面
        #读取文件
        self.pushButton.clicked.connect(self.msg)
        self.pushButton_2.clicked.connect(self.drawSpec)
        

    #实现绘图   
    def initUi(self):
            #self.layout = QHBoxLayout(self)
            
            self.mpl.start_static_plot()
            #self.mpl_ntb = NavigationToolbar(self.mpl, self)
            self.horizontalLayout.addWidget(self.mpl)       #将绘图部分封装入horizontallayout板块

    def drawSpec(self):
        '''plotPath = self.filePath[1] #list用[], ()是错误的无提示list not callable
        print(f"plotPath_name: {plotPath}")'''
        
        #通过删除控件来删除原来的图片
        self.horizontalLayout.removeWidget(self.mpl)
        self.mpl.deleteLater()

        #重新初始化绘图
        self.mpl = MyMplCanvas(self, width=5, height=4, dpi=100)
        self.mpl.start_item_plot(self.filePath)
        #self.delete_plot()
        self.horizontalLayout.addWidget(self.mpl)  
    



    #读取文件部分
    def msg(self):
        #读取多个文件
        self.filePath, _ = QFileDialog.getOpenFileNames(self, "选取文件", os.getcwd(), "*.*")
        print(f"File_name: {self.filePath}") 
        #格式化字符串，加f后可以在字符串里面使用用花括号括起来的变量和表达式，包含的{}表达式在程序运行时会被表达式的值代替
        self.Search_File(self.filePath)

    def Search_File(self,path):  #搜索与输入框关键词匹配的文件
        i = 0
        for file in path:
            sub_path = file  # 获取文件的绝对路径
            if (os.path.isdir(sub_path)):  # 判断是否为文件夹,如果是文件夹则忽略
                continue
                # temppath = os.listdir(sub_path)
                # self.Search_File(path)  # 递归调用函数，目的是遍历所有文件
            else:
                self.List_Data(i,file)
                i = i+1        

    def List_Data(self,i,data):  #将匹配成功的文件显示在界面上
            item = QtWidgets.QListWidgetItem()
            self.listWidget.addItem(item)
            item = self.listWidget.item(i)
            filename = os.path.basename(data)   #从绝对路径里提取文件名
            item.setText(filename)




    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainForm()
    myWin.show()
    sys.exit(app.exec_())
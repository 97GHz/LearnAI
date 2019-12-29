import sys
import copy
import numpy as np
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC

(GUI_X, GUI_Y, GUI_W, GUI_H) = (200, 200, 800, 600)
GUI_TITLE = "Decision Tree"

DATA_HEADER = ['outlook', 'temperature', 'humidity', 'windy', 'play']
DATA = [
    ['sunny', 'hot', 'high', 'FALSE', 'no'],
    ['sunny', 'hot', 'high', 'TRUE', 'no'],
    ['overcast', 'hot', 'high', 'FALSE', 'yes'],
    ['rainy', 'mild', 'high', 'FALSE', 'yes'],
    ['rainy', 'cool', 'normal', 'FALSE', 'yes'],
    ['rainy', 'cool', 'normal', 'TRUE', 'no'],
    ['overcast', 'cool', 'normal', 'TRUE', 'yes'],
    ['sunny', 'mild', 'high', 'FALSE', 'no'],
    ['sunny', 'cool', 'normal', 'FALSE', 'yes'],
    ['rainy', 'mild', 'normal', 'FALSE', 'yes'],
    ['sunny', 'mild', 'normal', 'TRUE', 'yes'],
    ['overcast', 'mild', 'high', 'TRUE', 'yes'],
    ['overcast', 'hot', 'normal', 'FALSE', 'yes'],
    ['rainy', 'mild', 'high', 'TRUE', 'no']
]


class DecisionTree(QWidget):
    def __init__(self):
        super().__init__()
        self.initParameter()
        self.initUI()
        self.setWindowTitle(GUI_TITLE)
        self.setGeometry(GUI_X, GUI_Y, GUI_W, GUI_H)
        self.show()

    def initUI(self):
        dataTable = QTableWidget(len(DATA), len(DATA_HEADER), self)
        dataTable.setHorizontalHeaderLabels(DATA_HEADER)
        self.setTableItems(dataTable)
        dataTable.resizeColumnsToContents()
        dataTable.setFixedWidth(330)
        dataTable.setFixedHeight(580)
        dataTable.move(10, 10)

        node1 = QLineEdit(self)
        node1.setFixedHeight(30)
        node1.move(530, 20)

        infoBrowser = QTextBrowser(self)
        infoBrowser.setFixedWidth(440)
        infoBrowser.setFixedHeight(190)
        infoBrowser.move(350, 400)
        self.infoBrowser = infoBrowser

    def initParameter(self):
        self.correctness = 100.0

    def setTableItems(self, table):
        for i, data in enumerate(DATA):
            for j, datum in enumerate(data):
                table.setItem(i, j, QTableWidgetItem(datum))

    def connectParameter(self):
        self.updateScreen()

    def updateInfo(self):
        self.infoBrowser.clear()
        self.infoBrowser.append('Correctness: {}%'.format(self.correctness))

    def updateScreen(self):
        self.updateInfo()
        self.repaint()

    def setClickEvent(self, event):
        pass
#        self.nextBtn.clicked.connect(event)

import sys
import copy
import math
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC

(GUI_X, GUI_Y, GUI_W, GUI_H) = (200, 200, 800, 600)
GUI_TITLE = "Decision Tree"

DATA_HEADER = ['outlook', 'temperature', 'humidity', 'windy', 'play']
DATA = [
    ['sunny', 'hot', 'high', 'FALSE', 'no'],
    ['sunny', 'hot', 'high', 'TRUE', 'no'],
    ['rainy', 'hot', 'high', 'FALSE', 'yes'],
    ['rainy', 'cool', 'high', 'FALSE', 'yes'],
    ['rainy', 'cool', 'normal', 'FALSE', 'yes'],
    ['rainy', 'cool', 'normal', 'TRUE', 'no'],
    ['sunny', 'cool', 'normal', 'TRUE', 'yes'],
    ['sunny', 'cool', 'high', 'FALSE', 'no'],
    ['sunny', 'cool', 'normal', 'FALSE', 'yes'],
    ['sunny', 'cool', 'normal', 'FALSE', 'yes'],
    ['rainy', 'hot', 'high', 'TRUE', 'yes'],
    ['rainy', 'hot', 'normal', 'FALSE', 'yes']
]
DATA_ATTRIBUTE = {
    'outlook': ['sunny', 'rainy'],
    'temperature': ['hot', 'cool'],
    'humidity': ['high', 'normal'],
    'windy': ['TRUE', 'FALSE'],
}


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
        node1.move(520, 20)
        self.node1 = node1

        node21 = QLineEdit(self)
        node21.setFixedHeight(30)
        node21.move(390, 130)
        self.node21 = node21

        node22 = QLineEdit(self)
        node22.setFixedHeight(30)
        node22.move(630, 130)
        self.node22 = node22

        infoRes1 = QTextBrowser(self)
        infoRes1.setFixedWidth(100)
        infoRes1.setFixedHeight(50)
        infoRes1.move(350, 230)
        self.infoRes1 = infoRes1

        infoRes2 = QTextBrowser(self)
        infoRes2.setFixedWidth(100)
        infoRes2.setFixedHeight(50)
        infoRes2.move(460, 230)
        self.infoRes2 = infoRes2

        infoRes3 = QTextBrowser(self)
        infoRes3.setFixedWidth(100)
        infoRes3.setFixedHeight(50)
        infoRes3.move(570, 230)
        self.infoRes3 = infoRes3

        infoRes4 = QTextBrowser(self)
        infoRes4.setFixedWidth(100)
        infoRes4.setFixedHeight(50)
        infoRes4.move(680, 230)
        self.infoRes4 = infoRes4

        nextBtn = QPushButton(self)
        nextBtn.setText("Calculate")
        nextBtn.setFixedWidth(100)
        nextBtn.setFixedHeight(40)
        nextBtn.move(680, 330)
        nextBtn.clicked.connect(self.clickBtn)

        infoBrowser = QTextBrowser(self)
        infoBrowser.setFixedWidth(440)
        infoBrowser.setFixedHeight(190)
        infoBrowser.move(350, 400)
        self.infoBrowser = infoBrowser

    def initParameter(self):
        self.correctness = 100.0
        self.branch1 = []
        self.branch21 = []
        self.branch22 = []

    def paintEvent(self, event):
        qp = QPainter(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(580, 50, 450, 130)
        qp.drawLine(580, 50, 690, 130)
        qp.drawLine(450, 160, 400, 230)
        qp.drawLine(450, 160, 510, 230)
        qp.drawLine(690, 160, 620, 230)
        qp.drawLine(690, 160, 730, 230)

        if self.branch1:
            qp.drawText(470, 90, self.branch1[0])
            qp.drawText(650, 90, self.branch1[1])
        if self.branch21:
            qp.drawText(380, 200, self.branch21[0])
            qp.drawText(490, 200, self.branch21[1])
        if self.branch22:
            qp.drawText(600, 200, self.branch22[0])
            qp.drawText(720, 200, self.branch22[1])
            pass

    def setTableItems(self, table):
        for i, data in enumerate(DATA):
            for j, datum in enumerate(data):
                table.setItem(i, j, QTableWidgetItem(datum))

    def connectParameter(self):
        self.updateScreen()

    def updateScreen(self):
        self.repaint()

    def calcEntropy(self, d):
        yes = d['yes']
        no = d['no']
        tot = yes + no
        yes /= tot
        no /= tot
        if yes == 0 or no == 0:
            S = 0
        else:
            S = -yes*math.log2(yes)-no*math.log2(no)
        return S

    def clickBtn(self, event):
        self.branch1 = []
        self.branch21 = []
        self.branch22 = []
        cnt = 0

        if self.node1.text() in DATA_ATTRIBUTE.keys():
            cnt += 1
            self.branch1 = DATA_ATTRIBUTE[self.node1.text()]

        if self.node21.text() in DATA_ATTRIBUTE.keys():
            cnt += 1
            self.branch21 = DATA_ATTRIBUTE[self.node21.text()]

        if self.node22.text() in DATA_ATTRIBUTE.keys():
            cnt += 1
            self.branch22 = DATA_ATTRIBUTE[self.node22.text()]

        if cnt >= 3:
            i = DATA_HEADER.index(self.node1.text())
            j = DATA_HEADER.index(self.node21.text())
            ans1 = {'yes': 0, 'no': 0}
            ans2 = {'yes': 0, 'no': 0}
            for d in DATA:
                if d[i] == self.branch1[0] and d[j] == self.branch21[0]:
                    ans1[d[4]] += 1
                if d[i] == self.branch1[0] and d[j] == self.branch21[1]:
                    ans2[d[4]] += 1

            j = DATA_HEADER.index(self.node21.text())
            ans3 = {'yes': 0, 'no': 0}
            ans4 = {'yes': 0, 'no': 0}
            for d in DATA:
                if d[i] == self.branch1[1] and d[j] == self.branch21[0]:
                    ans3[d[4]] += 1
                if d[i] == self.branch1[1] and d[j] == self.branch21[1]:
                    ans4[d[4]] += 1

            S = 0
            S += self.calcEntropy(ans1)
            S += self.calcEntropy(ans2)
            S += self.calcEntropy(ans3)
            S += self.calcEntropy(ans4)

            self.infoRes1.clear()
            self.infoRes2.clear()
            self.infoRes3.clear()
            self.infoRes4.clear()
            self.infoBrowser.clear()
            self.infoRes1.append('yes: {}'.format(ans1['yes']))
            self.infoRes1.append('no: {}'.format(ans1['no']))
            self.infoRes2.append('yes: {}'.format(ans2['yes']))
            self.infoRes2.append('no: {}'.format(ans2['no']))
            self.infoRes3.append('yes: {}'.format(ans3['yes']))
            self.infoRes3.append('no: {}'.format(ans3['no']))
            self.infoRes4.append('yes: {}'.format(ans4['yes']))
            self.infoRes4.append('no: {}'.format(ans4['no']))
            self.infoBrowser.append('Total Entropy: {}'.format(round(S, 3)))

        self.repaint()

import sys
import copy
import numpy as np
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC

(GUI_X, GUI_Y, GUI_W, GUI_H) = (200, 200, 800, 600)
GUI_TITLE = "Linear Regression"


def is_float(input):
    try:
        num = float(input)
    except ValueError:
        return False
    return True


class LinearRegression(QWidget):
    def __init__(self):
        super().__init__()
        self.initParameter()
        self.initUI()
        self.setWindowTitle(GUI_TITLE)
        self.setGeometry(GUI_X, GUI_Y, GUI_W, GUI_H)
        self.show()

    def initUI(self):
        self.fig = plt.Figure()
        self.canvas = FC(self.fig)

        layout = QHBoxLayout()
        toolBox = QVBoxLayout()

        infoBrowser = QTextBrowser()
        self.infoBrowser = infoBrowser

        learningRateBox = QHBoxLayout()

        learningRateLabel = QLabel('Learning Rate')
        learningRateInput = QLineEdit()
        learningRateInput.textChanged.connect(self.changeLearningRate)
        self.learningRateInput = learningRateInput

        nextBtn = QPushButton('Next')
        self.nextBtn = nextBtn

        learningRateBox.addWidget(learningRateLabel)
        learningRateBox.addWidget(learningRateInput)

        toolBox.addWidget(infoBrowser)
        toolBox.addLayout(learningRateBox)
        toolBox.addWidget(nextBtn)

        layout.addWidget(self.canvas)
        layout.addLayout(toolBox)

        self.layout = layout
        self.setLayout(self.layout)

    def initParameter(self):
        self.count = 0

    def connectParameter(self, x, y, w, b, cost, learningRate):
        self.x = x
        self.y = y
        self.w = w
        self.b = b
        self.cost = cost
        self.learningRate = learningRate
        self.learningRateInput.setText(str(self.learningRate[0]))
        self.updateScreen()

    def changeLearningRate(self):
        input = self.learningRateInput.text()
        if is_float(input):
            self.learningRate[0] = float(input)

    def updateInfo(self):
        self.count += 1
        self.infoBrowser.clear()
        self.infoBrowser.append('Count: {}'.format(self.count))
        self.infoBrowser.append('W: {}'.format(round(self.w[0], 3)))
        self.infoBrowser.append('B: {}'.format(round(self.b[0], 3)))
        self.infoBrowser.append('Prev Cost: {}'.format(round(self.cost[0], 3)))

    def updateGraph(self):
        self.fig.clear()

        x = np.asarray(self.x, dtype=np.float32)
        y = np.asarray(self.y, dtype=np.float32)

        y_bar = self.w[0] * x + self.b[0]

        ax = self.fig.add_subplot(111)
        ax.scatter(x, y)
        ax.plot(x, y_bar)

        ax.set_xlabel("x")
        ax.set_xlabel("y")
        ax.set_title(GUI_TITLE)
        self.canvas.draw()

    def updateScreen(self):
        self.updateGraph()
        self.updateInfo()
        self.repaint()

    def setClickEvent(self, event):
        self.nextBtn.clicked.connect(event)

import sys
import copy
import numpy as np
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC

(GUI_X, GUI_Y, GUI_W, GUI_H) = (200, 200, 800, 600)
GUI_TITLE = "Logistic Regression"
COMBO_BOX_TITLE = ['G(x) = sig(Wx+B) Graph', 'Cost(W,B) Graph']


def isFloat(input):
    try:
        num = float(input)
    except ValueError:
        return False
    return True


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


class LogisticRegression(QWidget):
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

        layout = QVBoxLayout()
        graphComboBox = QComboBox()
        for title in COMBO_BOX_TITLE:
            graphComboBox.addItem(title)
        graphComboBox.currentIndexChanged.connect(self.updateScreen)
        self.graphComboBox = graphComboBox

        contentLayout = QHBoxLayout()
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

        contentLayout.addWidget(self.canvas)
        contentLayout.addLayout(toolBox)

        layout.addLayout(contentLayout)
        layout.addWidget(graphComboBox)

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
        if isFloat(input):
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
        if self.graphComboBox.currentIndex() == 0:
            x = np.asarray(self.x, dtype=np.float32)
            y = np.asarray(self.y, dtype=np.float32)

            y_bar = self.w[0] * x + self.b[0]
            h = 1.0 / (1.0 + np.exp(-y_bar))

            ax = self.fig.add_subplot(111)
            ax.scatter(x, y)
            ax.plot(x, h)

            ax.set_xlabel("x")
            ax.set_xlabel("y")
            ax.set_title(GUI_TITLE)

        elif self.graphComboBox.currentIndex() == 1:
            w, b = self.w[0], self.b[0]
            W = np.arange(w-5, w+5, 0.2)
            B = np.arange(b-5, b+5, 0.2)
            W, B = np.meshgrid(W, B)
            C = np.zeros((50, 50))

            for (x, y) in zip(self.x, self.y):
                if y == 0:
                    C -= np.log(1-sigmoid(W*x+B))
                else:
                    C -= np.log(sigmoid(W*x+B))
            C /= len(self.x)

            ax = self.fig.gca(projection='3d')
            ax.plot_wireframe(W, B, C, color='black')
            ax.plot(self.w, self.b, self.cost, 'ro')
            ax.set_xlabel('W axis')
            ax.set_ylabel('B axis')
            ax.set_zlabel('Cost axis')
            ax.set_title(GUI_TITLE)

        self.canvas.draw()

    def updateScreen(self):
        self.updateGraph()
        self.updateInfo()
        self.repaint()

    def setClickEvent(self, event):
        self.nextBtn.clicked.connect(event)

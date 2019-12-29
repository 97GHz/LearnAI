import sys
import random
from PyQt5.QtWidgets import *
from LearnAI.LinearRegression import LinearRegression


def Calc():
    aw = 0
    ab = 0
    cost[0] = 0
    for (xi, yi) in zip(x, y):
        aw += (w[0] * xi + b[0] - yi) * xi
        ab += (w[0] * xi + b[0] - yi)
        cost[0] += (w[0] * xi + b[0] - yi) ** 2
    aw /= len(x)
    ab /= len(x)
    w[0] -= learningRate[0]*aw
    b[0] -= learningRate[0]*ab

    reg.updateScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    w = [random.uniform(-3, 3)]
    b = [random.uniform(-3, 3)]
    cost = [0]
    learningRate = [0.001]

    reg = LinearRegression()
    reg.setClickEvent(Calc)
    reg.connectParameter(x, y, w, b, cost, learningRate)

    app.exec_()

import sys
import math
import random
from PyQt5.QtWidgets import *
from LearnAI.LogisticRegression import LogisticRegression


def sigmoid(z):
    return 1.0/(1.0+math.exp(-z))


def Calc():
    aw = 0.0
    ab = 0.0
    cost[0] = 0
    for (xi, yi) in zip(x, y):
        z = w[0]*xi+b[0]
        s = sigmoid(z)
        if yi == 0:
            aw += s*xi
            ab += s
            cost[0] -= math.log(1-s)
        else:
            aw -= (1-s)*xi
            ab -= (1-s)
            cost[0] -= math.log(s)
    aw /= len(x)
    ab /= len(x)
    cost[0] /= len(x)
    w[0] -= learningRate[0]*aw
    b[0] -= learningRate[0]*ab

    reg.updateScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    w = [random.uniform(-3, 3)]
    b = [random.uniform(-3, 3)]
    cost = [0]
    learningRate = [0.1]

    reg = LogisticRegression()
    reg.setClickEvent(Calc)
    reg.connectParameter(x, y, w, b, cost, learningRate)

    app.exec_()

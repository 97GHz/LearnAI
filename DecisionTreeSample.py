import sys
from PyQt5.QtWidgets import *
from LearnAI.DecisionTree import DecisionTree


def Calc():
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    dt = DecisionTree()
    dt.setClickEvent(Calc)
    dt.connectParameter()

    app.exec_()

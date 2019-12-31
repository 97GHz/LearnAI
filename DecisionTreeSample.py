import sys
from PyQt5.QtWidgets import *
from LearnAI.DecisionTree import DecisionTree


if __name__ == '__main__':
    app = QApplication(sys.argv)

    dt = DecisionTree()

    app.exec_()

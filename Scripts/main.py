import os.path
import tkinter as tk
from app_qt import MainWindowUI
from EIOConverter import SignalsConverterToCfg, SignalsConverterToExcel
from PyQt5.QtWidgets import QApplication
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal


class Controller:

    def __init__(self, main_window):
        self.main_window = main_window
        print('controller')


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.view1 = MainWindowUI(self)
        self.controller = Controller(self)


def main():
    app = QApplication(sys.argv)

    application = MainWindow()
    application.show()
    app.exec()

if __name__ == '__main__':
    main()

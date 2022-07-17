import tkinter as tk
from app_qt import MainWindow
from EIOConverter import SignalsConverterToCfg, SignalsConverterToExcel
from PyQt5.QtWidgets import QApplication
import sys


class MainApp():

    def __init__(self):
        self.conversion_to = None


def main():

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()







if __name__ == '__main__':
    main()

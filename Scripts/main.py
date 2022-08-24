import os.path
import tkinter as tk
from app_qt import MainWindow
from EIOConverter import SignalsConverterToCfg, SignalsConverterToExcel
from PyQt5.QtWidgets import QApplication
import settings
import sys


class MainApp(MainWindow):

    def __init__(self):
        super().__init__()
        self.window = MainWindow()
        self.window.show()


def main():

    settings.init()
    app = QApplication(sys.argv)

    application = MainApp()
    #application.convert_file()
    app.exec()

if __name__ == '__main__':
    main()

import os.path
import tkinter as tk
from app_qt import MainWindowUI
from EIOConverter import SignalsConverterToCfg, SignalsConverterToExcel
from PyQt5.QtWidgets import QApplication
import sys

class MainApp():

    def __init__(self):
        super().__init__()
        self.window = MainWindowUI()
        self.window.show()
        # self.convert_obj = None
        # self.directory_to_save = None
        # self.file_path_to_save = None
        # self._destination_file = None
        # self.destination_file = None

def main():

    app = QApplication(sys.argv)

    application = MainApp()
    #application.convert_file()
    app.exec()

if __name__ == '__main__':
    main()

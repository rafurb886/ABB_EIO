import os.path
import tkinter as tk
from app_qt import MainWindow
from EIOConverter import SignalsConverterToCfg, SignalsConverterToExcel
from PyQt5.QtWidgets import QApplication
import sys


class MainApp(MainWindow):

    def __init__(self):
        super().__init__()
        self.window = MainWindow()
        self.window.show()
        self.convert_obj = None
        self.directory_to_save = None
        self.file_path_to_save = None
        self._destination_file = None
        self.destination_file = None


    def convert_file(self):
        if self.conversion_to == 'xlsx':
            self.convert_obj = SignalsConverterToCfg.from_excel()
        elif self.conversion_to == 'cfg':
            self.convert_obj = SignalsConverterToExcel.from_cfg()
        #self.destination_file = self.set_destination_file()
        self.convert_obj.convert(self.destination_file)




def main():

    app = QApplication(sys.argv)

    application = MainApp()
    #application.convert_file()
    app.exec()







if __name__ == '__main__':
    main()

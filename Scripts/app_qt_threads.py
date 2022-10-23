from PyQt5.QtWidgets import QApplication, \
                            QLabel, \
                            QWidget, \
                            QMainWindow, \
                            QPushButton, \
                            QVBoxLayout, \
                            QHBoxLayout, \
                            QLineEdit
from PyQt5.QtCore import Qt, QDir, QObject, QThread, pyqtSignal, pyqtSlot

import time
import settings


class UserInterfaceToNewParams(QObject):

    def run(self):
        print('jestem 1')


class ThreadConversion(QObject):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def run(self):
        print('Thread conversion')
        self.main_window.view1.line_edit_new_param.setVisible(True)

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
    show_edit_line = pyqtSignal()

    # def __init__(self, main_window):
    #     super().__init__()
    #     self.main_window = main_window
    #     print('thread')

    def run(self):
        print('jestem 1')
        # while True:
        #     if settings.global_waiting_for_user_new_param:
        #         self.show_edit_line.emit()
        #         print('jestem 2')
        #
        #         settings.global_waiting_for_user_new_param = False
        #     time.sleep(0.5)


class ThreadConversion(QObject):

    def run(self):
        print('Thread conversion')
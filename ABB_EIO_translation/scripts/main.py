import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from ABB_EIO_translation.scripts.app_qt import MainWindowUI


class Controller:

    def __init__(self, main_window):
        self.main_window = main_window
        print('controller')


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.view1 = MainWindowUI(self)
        self.controller = Controller(self)

    def shutdown(self):
        if self.view1.thread_to_conversion:  # set self.runner=None in your __init__ so it's always defined.
            self.view1.thread_to_conversion.stop()


def main():
    app = QApplication(sys.argv)
    application = MainWindow()
    application.show()
    app.aboutToQuit.connect(application.shutdown)
    app.exec()


if __name__ == '__main__':
    main()

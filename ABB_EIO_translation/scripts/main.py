import sys

from PyQt5 import QtWidgets
from ABB_EIO_translation.scripts.errors import ApplicationError
from PyQt5.QtWidgets import QApplication, QMainWindow

from ABB_EIO_translation.scripts.app_qt import MainWindowUI



class Controller:

    def __init__(self, main_window):
        self.main_window = main_window


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.view1 = MainWindowUI(self)
        self.controller = Controller(self)

    def shutdown(self):
        if self.view1.thread_to_conversion:  # set self.runner=None in your __init__ so it's always defined.
            self.view1.thread_to_conversion.stop()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.view1.label_to_many_files.setVisible(False)
        self.view1.label_wrong_file_type.setVisible(False)

        if len(event.mimeData().urls()) > 1:
            self.view1.label_to_many_files.setVisible(True)
        else:
            self.view1.file_path = event.mimeData().urls()[0].toLocalFile()
            self.view1.get_file_to_convert()

def main():
    app = QApplication(sys.argv)
    application = MainWindow()
    application.show()
    app.aboutToQuit.connect(application.shutdown)
    app.exec()


if __name__ == '__main__':
    main()

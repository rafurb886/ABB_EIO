import os.path
import tkinter as tk
from app_qt import MainWindowUI
from EIOConverter import SignalsConverterToCfg, SignalsConverterToExcel
from PyQt5.QtWidgets import QApplication
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal


class MainApp():

    def __init__(self):
        super().__init__()
        self.window = MainWindowUI()
        self.window.show()


class Controller():

    def __init__(self, main_window):
        self.main_window = main_window
        print('controller')

    def on_item_added(self, guid):
        view1 = self.main_window.view1
        model = self.main_window.model

        print("item guid={0} added".format(guid))
        item = model.items[guid]
        x, y = item["pos"]
        graphics_item = QtWidgets.QGraphicsEllipseItem(x, y, 60, 40)
        item["graphics_item"] = graphics_item
        view1.scene.addItem(graphics_item)

    def on_item_removed(self, guid):
        if guid < 0:
            print("global cache of items is empty")
        else:
            view1 = self.main_window.view1
            model = self.main_window.model

            item = model.items[guid]
            x, y = item["pos"]
            graphics_item = item["graphics_item"]
            view1.scene.removeItem(graphics_item)
            print("item guid={0} removed".format(guid))

    def show_edit_line_new_param_input(self, question):
        view = self.main_window.view1
        view.line_edit_new_param.setVisible(True)


class MainWindow(QtWidgets.QMainWindow):
    signal_show_edit_line_to_new_param = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.converted_obj = SignalsConverterToCfg()
        #self.model_to_excel = SignalsConverterToExcel()

        self.view1 = MainWindowUI(self)

        self.controller = Controller(self)

        self.attach_views_to_model()

    def attach_views_to_model(self):
        self.converted_obj.signal_show_edit_line_to_new_param.connect(self.view1.get_new_param)
        #self.model_to_cfg.show_edit_line_to_new_param.connect(self.controller.show_edit_line_new_param_input)
        #self.model_to_cfg.item_removed.connect(self.controller.on_item_removed)


def main():
    app = QApplication(sys.argv)

    application = MainWindow()
    application.show()
    app.exec()

if __name__ == '__main__':
    main()

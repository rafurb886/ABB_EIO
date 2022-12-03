from PyQt5.QtWidgets import QApplication, \
                            QLabel, \
                            QWidget, \
                            QMainWindow, \
                            QPushButton, \
                            QVBoxLayout, \
                            QHBoxLayout, \
                            QLineEdit,\
                            QCheckBox
from PyQt5.QtCore import Qt, pyqtSignal
from .app_qt_styles import *
import sys
from . import settings


class DialogWindowWhenFileExist(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("File Exist")
        self.setAutoFillBackground(True)
        self.setFixedSize(400, 300)
        self.setStyleSheet(style_main_screen)

        self.label_description = QLabel('File exist choose action:')
        self.label_description.setStyleSheet(style_description_label)
        self.check_box_override_all_file = QCheckBox('Override all file')
        self.check_box_override_all_file.setStyleSheet(style_checkbox)
        self.check_box_override_signals = QCheckBox('Override signals')
        self.check_box_override_signals.setStyleSheet(style_checkbox)
        self.check_box_append_signals = QCheckBox('Append signals')
        self.check_box_append_signals.setStyleSheet(style_checkbox)
        self.button_apply_selection = QPushButton('Ok')
        self.button_apply_selection.setStyleSheet(style_button)
        self.button_apply_selection.move
        self.button_apply_selection.setDisabled(True)

        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(self.label_description)
        self.layout_main.addWidget(self.check_box_override_all_file)
        self.layout_main.addWidget(self.check_box_override_signals)
        self.layout_main.addWidget(self.check_box_append_signals)
        self.layout_main.addWidget(self.button_apply_selection)
        self.setLayout(self.layout_main)

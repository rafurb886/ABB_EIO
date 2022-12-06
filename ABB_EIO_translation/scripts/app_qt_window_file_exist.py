from PyQt5.QtWidgets import QApplication, \
                            QLabel, \
                            QWidget, \
                            QDialog,\
                            QMainWindow, \
                            QPushButton, \
                            QVBoxLayout, \
                            QHBoxLayout, \
                            QLineEdit,\
                            QRadioButton,\
                            QCheckBox
from PyQt5.QtCore import Qt, pyqtSignal
from .app_qt_styles import *
import numpy as np
import sys
from . import settings


class DialogWindowWhenFileExist(QDialog):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.during_changing = False
        self.setAutoFillBackground(True)
        self.setFixedSize(400, 300)
        self.setStyleSheet(style_dialog_screen)
        self.setModal(True)

        self.label_description = QLabel('File exist choose action:')
        self.label_description.setStyleSheet(style_description_label)
        self.label_description.setFixedSize(10, 30)
        self.override_all_file = QRadioButton('Override all file')
        self.override_all_file.setStyleSheet(style_checkbox)
        self.override_signals = QRadioButton('Override signals')
        self.override_signals.setStyleSheet(style_checkbox)
        self.append_signals = QRadioButton('Append signals')
        self.append_signals.setStyleSheet(style_checkbox)
        self.override_all_file.toggled.connect(lambda: self.set_only_one_checkbox(self.override_all_file))
        self.override_signals.toggled.connect(lambda: self.set_only_one_checkbox(self.override_signals))
        self.append_signals.toggled.connect(lambda: self.set_only_one_checkbox(self.append_signals))

        self.button_apply_selection = QPushButton('Ok')
        self.button_apply_selection.setStyleSheet(style_button)
        self.button_apply_selection.clicked.connect(self.acknowledge_button)
        self.button_apply_selection.setDisabled(True)

        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(self.label_description)
        self.layout_main.addWidget(self.override_all_file)
        self.layout_main.addWidget(self.override_signals)
        self.layout_main.addWidget(self.append_signals)
        self.layout_main.addWidget(self.button_apply_selection, alignment=Qt.AlignRight)
        self.setLayout(self.layout_main)

        self.boxes_to_check = {self.override_all_file: 'override_all_file',
                               self.override_signals: 'override_signals',
                               self.append_signals: 'append_to_signals'}

    def set_only_one_checkbox(self, checkbox):
        if not self.during_changing:
            self.during_changing = True
            for box in self.boxes_to_check.keys():
                if box is checkbox:
                    box.setChecked(True)
                else:
                    box.setChecked(False)
            self.activate_acknowledge_button()
            self.during_changing = False

    def activate_acknowledge_button(self):
        if any(x.isChecked() for x in self.boxes_to_check.keys()):
            self.button_apply_selection.setDisabled(False)

    def acknowledge_button(self):
        self.where_to_add_signals = [value for key, value in self.boxes_to_check.items() if key.isChecked()][0]
        self.setVisible(False)



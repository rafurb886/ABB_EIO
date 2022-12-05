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
        self.check_box_override_all_file = QRadioButton('Override all file')
        self.check_box_override_all_file.setStyleSheet(style_checkbox)
        self.check_box_override_signals = QRadioButton('Override signals')
        self.check_box_override_signals.setStyleSheet(style_checkbox)
        self.check_box_append_signals = QRadioButton('Append signals')
        self.check_box_append_signals.setStyleSheet(style_checkbox)
        self.check_box_override_all_file.toggled.connect(lambda: self.set_only_one_checkbox(self.check_box_override_all_file))
        self.check_box_override_signals.toggled.connect(lambda: self.set_only_one_checkbox(self.check_box_override_signals))
        self.check_box_append_signals.toggled.connect(lambda: self.set_only_one_checkbox(self.check_box_append_signals))

        self.button_apply_selection = QPushButton('Ok')
        self.button_apply_selection.setStyleSheet(style_button)
        self.button_apply_selection.clicked.connect(self.acknowledge_button)
        self.button_apply_selection.setDisabled(True)

        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(self.label_description)
        self.layout_main.addWidget(self.check_box_override_all_file)
        self.layout_main.addWidget(self.check_box_override_signals)
        self.layout_main.addWidget(self.check_box_append_signals)
        self.layout_main.addWidget(self.button_apply_selection, alignment=Qt.AlignRight)
        self.setLayout(self.layout_main)

    def set_only_one_checkbox(self, checkbox):
        if not self.during_changing:
            self.during_changing = True
            if checkbox == self.check_box_override_all_file:
                self.check_box_override_all_file.setChecked(True)
                self.check_box_append_signals.setChecked(False)
                self.check_box_override_signals.setChecked(False)
            if checkbox == self.check_box_override_signals:
                self.check_box_override_signals.setChecked(True)
                self.check_box_append_signals.setChecked(False)
                self.check_box_override_all_file.setChecked(False)
            if checkbox == self.check_box_append_signals:
                self.check_box_append_signals.setChecked(True)
                self.check_box_override_all_file.setChecked(False)
                self.check_box_override_signals.setChecked(False)
            self.activate_acknowledge_button()
            self.during_changing = False

    def activate_acknowledge_button(self):
        if any([self.check_box_override_all_file.isChecked(),
                self.check_box_override_signals.isChecked(),
                self.check_box_append_signals.isChecked()]):
            self.button_apply_selection.setDisabled(False)

    def acknowledge_button(self):
        self.setVisible(False)


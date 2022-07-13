import os.path

from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, \
    QPushButton, QAction, QMenu, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout, QCheckBox
from PyQt5.QtCore import Qt, QSize

import sys


available_extension = ['.png', '.xlsx']
# COLORS IN RGB
color_background = f'rgb(187, 187, 167)'
color_background_label = f'rgb(187, 187, 167)'
color_background_button_hover = f'rgb(120, 120, 120)'
color_background_button = f'rgb(140, 140, 140)'
color_border_of_buttons = f'rgb(83, 83, 83)'
color_border_of_labels = f'rgb(130, 130, 130)'
color_font_title = f'rgb(83, 83, 83)'
color_font_header = f'rgb(83, 83, 83)'
color_font_text = f'rgb(35, 35, 35)'

style_main_screen = f" background-color: {color_background};"
style_mian_widget = f" padding :140px;"
style_description_label = f" background-color: {color_background_label};" \
                          f" color: {color_font_text};" \
                          f" font-size: 25px;" \
                          f" font: bold italic 'Times New Roman';" \
                          f" min-width: 600px;" \
                          f" text-align: left;"
style_button =      f"QPushButton {{background-color: {color_background_button};" \
                    f" color: {color_font_text};" \
                    f" font-size: 25px;" \
                    f" font: bold italic 'Times New Roman';" \
                    f" max-width: 300px;" \
                    f" text-align: center;" \
                    f" padding :10px;" \
                    f" }}" \
                    f" QPushButton:hover {{"\
                    f" background-color: {color_background_button_hover};" \
                    f" color: {color_font_text}" \
                    f"}}"
style_check_box =   f" QCheckBox {{"\
                    f" color: {color_font_text};" \
                    f" font-size: 25px;" \
                    f" font: bold italic 'Times New Roman';" \
                    f" max-width: 300px;" \
                    f" text-align: center;" \
                    f" padding :10px;" \
                    f" }}"

style_label_error =         f" QLabel {{"\
                            f" background-color: {color_background_label};" \
                            f" color: FireBrick;" \
                            f" font-size: 15px;" \
                            f" font: bold italic 'Times New Roman';" \
                            f" max-width: 500px;" \
                            f" qproperty-alignment: AlignCenter;"\
                            f" border: 2px solid FireBrick"\
                            f"}}"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        " normal application variable"
        self.path_to_file = None
        "end"

        self.chosen_conversation_type = None
        self.setWindowTitle("My App")
        self.setAutoFillBackground(True)
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet(style_main_screen)
        self.setAcceptDrops(True)

        "LABELS"
        self.label_description = QLabel()
        self.label_description.setText( 'Chose your action or directly select your file.<br>'\
                                        'You can drag and drop your file')
        self.label_description.setFixedHeight(100)
        self.label_description.setAlignment(Qt.AlignTop)
        self.label_description.setStyleSheet(style_description_label)

        "CHECK BOX"
        self.button_to_cfg = QCheckBox('Convert excel to .cfg', )
        self.button_to_cfg.setStyleSheet(style_check_box)
        self.button_to_cfg.toggled.connect(lambda: self.button_to_cfg_toggled(self.button_to_cfg))

        self.button_to_excel = QCheckBox('Convert excel to .xlsx')
        self.button_to_excel.setStyleSheet(style_check_box)
        self.button_to_excel.toggled.connect(lambda: self.button_to_excel_toggled(self.button_to_excel))

        self.label_to_many_files = QLabel('To many files!!!   Select only one')
        self.label_to_many_files.setStyleSheet(style_label_error)
        self.label_to_many_files.setVisible(False)

        self.label_wrong_file_type = QLabel(f'Wrong type of file. Available files {available_extension}')
        self.label_wrong_file_type.setStyleSheet(style_label_error)
        self.label_wrong_file_type.setVisible(False)

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.button_to_cfg)
        self.button_layout.addWidget(self.button_to_excel)
        self.button_layout.addWidget(self.label_to_many_files)
        self.button_layout.addWidget(self.label_wrong_file_type)


        self.main_window_layout = QVBoxLayout()
        self.main_window_layout.setSpacing(20)
        self.main_window_layout.setContentsMargins(20, 20, 20, 20)
        self.main_window_layout.setAlignment(Qt.AlignTop)
        self.main_window_layout.addWidget(self.label_description)
        self.main_window_layout.addLayout(self.button_layout)


        self.w = QWidget()
        self.w.setLayout(self.main_window_layout)
        self.setCentralWidget(self.w)


    def button_to_cfg_toggled(self, button):
        if button.isChecked():
            self.chosen_conversation_type = 'to_cfg'
            self.button_to_excel.setChecked(False)
        else:
            self.chosen_conversation_type = None

    def button_to_excel_toggled(self, button):
        if button.isChecked():
            self.chosen_conversation_type = 'to_excel'
            self.button_to_cfg.setChecked(False)
        else:
            self.chosen_conversation_type = None


    def mouseMoveEvent(self, e):
        self.label_description.setText("mouseMoveEvent")

    def mousePressEvent(self, e):
        self.label_description.setText("mousePressEvent")


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.label_to_many_files.setVisible(False)
        self.label_wrong_file_type.setVisible(False)

        if len(event.mimeData().urls()) > 1:
            print('to many files')
            self.label_to_many_files.setVisible(True)
        else:
            self.path_to_file = event.mimeData().urls()[0].toLocalFile()
            self._file_name, self._file_extension = os.path.splitext(self.path_to_file)
            print(self.path_to_file)
            if self._file_extension not in available_extension:
                self.label_wrong_file_type.setVisible(True)
                self.path_to_file = None




if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()




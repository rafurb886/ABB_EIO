from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, \
    QPushButton, QAction, QMenu, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout, QCheckBox
from PyQt5.QtCore import Qt, QSize

import sys

# COLORS IN RGB
color_background = f'rgb(34, 61, 108)'
color_background_label = f'rgb(183, 183, 160)'
color_background_button_realesed = f'rgb(183, 183, 160)'
color_background_button_pressed = f'rgb(183, 183, 160)'
color_font_title = f'rgb(83, 83, 83)'
color_font_header = f'rgb(83, 83, 83)'
color_font_text = f'rgb(35, 35, 35)'

style_main_screen = f"background-color: {color_background}"
style_description_label = f"background-color: {color_background_label};" \
                          f" color: {color_font_text};" \
                          f" border-radius: 15px;" \
                          f" font-size: 25px;" \
                          f" font: bold italic 'Times New Roman';" \
                          f" min-width: 100px;" \
                          f" text-align: left;"
style_button = f"QPushButton {{background-color: {color_background_label};" \
                    f" color: {color_font_text};" \
                    f" border-radius: 5px;" \
                    f" font-size: 25px;" \
                    f" font: bold italic 'Times New Roman';" \
                    f" min-width: 100px;" \
                    f" text-align: left;" \
                f"}}" \
                f"QPushButton:hover {{"\
                    f"color: {color_background}" \
                f"}}"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setAutoFillBackground(True)
        self.setGeometry(300, 100, 1000, 600)
        self.setStyleSheet(style_main_screen)

        "LABELS"
        self.label_description = QLabel()
        self.label_description.setText('Chose your action and select your file.')
        self.label_description.setFixedHeight(100)
        self.label_description.setAlignment(Qt.AlignLeft)
        self.label_description.setStyleSheet(style_description_label)

        self.button_to_cfg = QPushButton('Convert excel to .cfg')
        self.button_to_cfg.setStyleSheet(style_button)

        self.main_window_layout = QVBoxLayout()
        self.main_window_layout.addWidget(self.label_description)
        self.main_window_layout.addWidget(self.button_to_cfg)

        #self.main_window_layout.set




        self.w = QWidget()
        self.w.setLayout(self.main_window_layout)
        #self.w.setBackgroundRole(color_background)
        self.setCentralWidget(self.w)

    def mouseMoveEvent(self, e):
        self.label_description.setText("mouseMoveEvent")

    def mousePressEvent(self, e):
        self.label_description.setText("mousePressEvent")

    # uncheck method
    def uncheck(self, state):

        # checking if state is checked
        if state == Qt.Checked:

            # if first check box is selected
            if self.sender() == self.checkBoxNone:

                # making other check box to uncheck
                self.checkBoxA.setChecked(False)
                self.checkBoxB.setChecked(False)

            # if second check box is selected
            elif self.sender() == self.checkBoxA:

                # making other check box to uncheck
                self.checkBoxNone.setChecked(False)
                self.checkBoxB.setChecked(False)

            # if third check box is selected
            elif self.sender() == self.checkBoxB:

                # making other check box to uncheck
                self.checkBoxNone.setChecked(False)
                self.checkBoxA.setChecked(False)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()




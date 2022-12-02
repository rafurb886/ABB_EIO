import sys

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

from ABB_EIO_translation.scripts.app_qt_styles import *
from ABB_EIO_translation.scripts.app_qt_helper_main_window import QtAppHelper
from ABB_EIO_translation.scripts import settings


class MainSignals:
    show_window_user_decision_if_file_exist = pyqtSignal()
    user_decided_if_file_exist = pyqtSignal(int)


class MainWindowUI(QtAppHelper):

    def __init__(self, main_window):
        super().__init__(self, main_window)
        settings.global_qt_app_run = True
        self.main_window = main_window
        self.signals = MainSignals
        self.dialog_window_file_exist = None

        "LABELS"
        self.label_description = QLabel()
        self.label_description.setText('Select your file.<br>'
                                       'Available .xlsx or .cfg <br>')
        self.label_description.setFixedHeight(100)
        self.label_description.setAlignment(Qt.AlignTop)
        self.label_description.setStyleSheet(style_description_label)

        self.label_to_many_files = QLabel('To many files!!!   Select only one')
        self.label_to_many_files.setStyleSheet(style_label_error)
        self.label_to_many_files.setVisible(False)

        self.label_application_error = QLabel('Error')
        self.label_application_error.setStyleSheet(style_label_error)
        self.label_application_error.setVisible(False)

        self.label_wrong_file_type = QLabel(f'Wrong type of file. Available files {self.CONVERTER_CONST.AVAILABLE_EXTENSION}')
        self.label_wrong_file_type.setStyleSheet(style_label_error)
        self.label_wrong_file_type.setVisible(False)

        self.label_no_file_to_convert = QLabel(f'Chose file!')
        self.label_no_file_to_convert.setStyleSheet(style_label_error)
        self.label_no_file_to_convert.setVisible(False)

        self.label_chose_correct_file = QLabel(f'Chose correct file!')
        self.label_chose_correct_file.setStyleSheet(style_label_error)
        self.label_chose_correct_file.setVisible(False)

        self.label_chose_correct_destination_file = QLabel(f'Chose correct destiantion file!')
        self.label_chose_correct_destination_file.setStyleSheet(style_label_error)
        self.label_chose_correct_destination_file.setVisible(False)

        self.label_drag_and_drop = QLabel('Drag and Drop')
        self.label_drag_and_drop.setStyleSheet(style_drag_and_drop_label)
        self.label_drag_and_drop.setAcceptDrops(True)

        self.label_select_file_to_convert = QLabel('Select file:')
        self.label_select_file_to_convert.setStyleSheet(style_select_file)
        self.label_select_file_to_convert.setVisible(True)
        self.lineEdit_browse_file = QLineEdit()
        self.lineEdit_browse_file.setStyleSheet(style_edit_line_browse_file)
        self.button_browse_file = QPushButton('Search')
        self.button_browse_file.clicked.connect(self.browse_file_to_convert)
        self.button_browse_file.setStyleSheet(style_button)

        self.label_select_destination_file = QLabel('Select destination file:')
        self.label_select_destination_file.setStyleSheet(style_select_file)
        self.label_select_destination_file.setVisible(True)
        self.lineEdit_browse_file_2 = QLineEdit()
        self.lineEdit_browse_file_2.setStyleSheet(style_edit_line_browse_file)
        self.button_browse_file_2 = QPushButton('Browse')
        self.button_browse_file_2.clicked.connect(self.get_destination_file)
        self.button_browse_file_2.setStyleSheet(style_button)

        self.button_convert = QPushButton('Convert')
        self.button_convert.clicked.connect(self.convert_file)
        self.button_convert.setStyleSheet(style_button)

        self.label_conversion_finished_successful = QLabel(f'Conversion finished successful!')
        self.label_conversion_finished_successful.setStyleSheet(style_label_successful)
        self.label_conversion_finished_successful.setVisible(False)

        self.label_conversion_finished_failure = QLabel(f'Conversion error, something went wrong!')
        self.label_conversion_finished_failure.setStyleSheet(style_label_error)
        self.label_conversion_finished_failure.setVisible(False)

        self.layout_browse_file = QHBoxLayout()
        self.layout_browse_file.addWidget(self.lineEdit_browse_file)
        self.layout_browse_file.addWidget(self.button_browse_file)

        self.layout_browse_file_2 = QHBoxLayout()
        self.layout_browse_file_2.addWidget(self.lineEdit_browse_file_2)
        self.layout_browse_file_2.addWidget(self.button_browse_file_2)

        self.layout_chose_file = QVBoxLayout()
        self.layout_chose_file.addWidget(self.label_application_error)
        self.layout_chose_file.addWidget(self.label_select_file_to_convert)
        self.layout_chose_file.addLayout(self.layout_browse_file)
        self.layout_chose_file.addWidget(self.label_select_destination_file)
        self.layout_chose_file.addLayout(self.layout_browse_file_2)

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.label_to_many_files)
        self.button_layout.addWidget(self.label_wrong_file_type)
        self.button_layout.addWidget(self.label_no_file_to_convert)
        self.button_layout.addWidget(self.label_chose_correct_file)
        self.button_layout.addWidget(self.label_chose_correct_destination_file)

        self.label_wrong_param = QLabel(f'Wrong param!')
        self.label_wrong_param.setStyleSheet(style_label_error)
        self.label_wrong_param.setVisible(False)
        self.label_conversion_finished = QLabel(f'Conversion finished successfully!')
        self.label_conversion_finished.setStyleSheet(style_label_successful)
        self.label_conversion_finished.setVisible(False)
        self.label_info_wrong_param = QLabel('info')
        self.label_info_wrong_param.setStyleSheet(style_select_file)
        self.label_info_wrong_param.setVisible(False)
        self.line_edit_new_param = QLineEdit()
        self.line_edit_new_param.setStyleSheet(style_edit_line_browse_file)
        self.line_edit_new_param.setVisible(False)
        self.button_new_param = QPushButton('Apply')
        self.button_new_param.clicked.connect(self.get_new_param)
        self.button_new_param.setStyleSheet(style_button)
        self.button_new_param.setVisible(False)
        self.label_new_param_ok = QLabel('New parameter ok')
        self.label_new_param_ok.setStyleSheet(style_label_successful)
        self.label_new_param_ok.setVisible(False)
        self.layout_new_param_top = QHBoxLayout()
        self.layout_new_param_top.addWidget(self.line_edit_new_param)
        self.layout_new_param_top.addWidget(self.button_new_param)
        self.layout_new_param = QVBoxLayout()
        self.layout_new_param.addWidget(self.label_conversion_finished)
        self.layout_new_param.addWidget(self.label_wrong_param)
        self.layout_new_param.addWidget(self.label_info_wrong_param)
        self.layout_new_param.addLayout(self.layout_new_param_top)
        self.layout_new_param.addWidget(self.label_new_param_ok)

        self.layout_chose = QHBoxLayout()
        self.layout_chose.addLayout(self.button_layout)
        self.layout_chose.addWidget(self.label_drag_and_drop)

        self.main_window_layout = QVBoxLayout()
        self.main_window_layout.setSpacing(20)
        self.main_window_layout.setContentsMargins(20, 20, 20, 20)
        self.main_window_layout.setAlignment(Qt.AlignTop)
        self.main_window_layout.addWidget(self.label_description)
        self.main_window_layout.addLayout(self.layout_chose)
        self.main_window_layout.addLayout(self.layout_chose_file)
        self.main_window_layout.addWidget(self.button_convert)
        # settings.line_edit_new_param.setVisible(True)
        self.main_window_layout.addLayout(self.layout_new_param)
        self.main_window_layout.addWidget(self.label_conversion_finished_failure)
        self.main_window_layout.addWidget(self.label_conversion_finished_successful)

        self.w = QWidget()
        self.w.setLayout(self.main_window_layout)
        self.main_window.setCentralWidget(self.w)
        self.main_window.setWindowTitle("My App")
        self.main_window.setAutoFillBackground(True)
        self.main_window.setGeometry(100, 100, 1000, 600)
        self.main_window.setStyleSheet(style_main_screen)

    def define_signals(self):
        self.signals.show_window_user_decision_if_file_exist.connect(self.show_dialog_when_file_exist)
        self.signals.user_decided_if_file_exist.connect(self.user_decided_if_file_exist)

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
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            self.get_file_to_convert()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    window = MainWindowUI()
    window.setupUi(MainWindow)
    MainWindow.show()
    app.exec()




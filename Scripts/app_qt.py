from PyQt5.QtWidgets import QApplication, \
                            QLabel, \
                            QWidget, \
                            QMainWindow, \
                            QPushButton, \
                            QVBoxLayout, \
                            QHBoxLayout, \
                            QLineEdit
from PyQt5.QtCore import Qt, QDir, QObject, QThread, pyqtSignal, pyqtSlot
from app_qt_styles import *
from app_qt_helper import QtAppHelper
from app_qt_threads import *
from app_qt_data import *
import sys, time
import settings



class MainWindow(QMainWindow, QtAppHelper):
    def __init__(self):
        super().__init__()

        settings.global_qt_app_run = True
        " normal application variable"
        self.file_path = None
        self.filter_name = 'All files (*.*)'
        self.filter_destination_name = 'Files (*.cfg *.xlsx)'
        self.dir_path = QDir.currentPath()
        self.destination_file = ''
        self.conversion_to = ''
        self._destination_file_name = {'xlsx': 'converted_xlsx',
                                       'cfg': 'converted_cfg'}
        self._destination_file_extension = {'xlsx': 'xlsx',
                                            'cfg': 'cfg'}
        self.default_destination_file = ''
        "end"

        self.chosen_conversation_type = None
        self.setWindowTitle("My App")
        self.setAutoFillBackground(True)
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet(style_main_screen)
        self.setAcceptDrops(True)

        self.thread_user_interface = QThread()
        self.user_interface_to_new_param = UserInterfaceToNewParams()
        self.user_interface_to_new_param.moveToThread(self.thread_user_interface)
        self.thread_user_interface.started.connect(self.user_interface_to_new_param.run)
        self.user_interface_to_new_param.show_edit_line.connect(self.show_edit_line_to_new_param)
        self.thread_user_interface.start()

        "LABELS"
        self.label_description = QLabel()
        self.label_description.setText( 'Chose your action or directly select your file.<br>'\
                                        'You can drag and drop your file')
        self.label_description.setFixedHeight(100)
        self.label_description.setAlignment(Qt.AlignTop)
        self.label_description.setStyleSheet(style_description_label)

        self.label_to_many_files = QLabel('To many files!!!   Select only one')
        self.label_to_many_files.setStyleSheet(style_label_error)
        self.label_to_many_files.setVisible(False)

        self.label_wrong_file_type = QLabel(f'Wrong type of file. Available files {available_extension}')
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

        self.label_select_file_to_convert = QLabel('Select file:')
        self.label_select_file_to_convert.setStyleSheet(style_select_file)
        self.label_select_file_to_convert.setVisible(True)
        self.lineEdit_browse_file = QLineEdit(self)
        self.lineEdit_browse_file.setStyleSheet(style_edit_line_browse_file)
        self.button_browse_file = QPushButton('Search')
        self.button_browse_file.clicked.connect(self.browse_file_to_convert)
        self.button_browse_file.setStyleSheet(style_button_search_file)

        self.label_select_destination_file = QLabel('Select destination file:')
        self.label_select_destination_file.setStyleSheet(style_select_file)
        self.label_select_destination_file.setVisible(True)
        self.lineEdit_browse_file_2 = QLineEdit(self)
        self.lineEdit_browse_file_2.setStyleSheet(style_edit_line_browse_file)
        self.button_browse_file_2 = QPushButton('Browse')
        self.button_browse_file_2.clicked.connect(self.get_destination_file)
        self.button_browse_file_2.setStyleSheet(style_button_search_file)

        self.button_convert = QPushButton('Convert')
        self.button_convert.clicked.connect(self.convert_file)
        self.button_convert.setStyleSheet(style_button_convert)

        self.label_inform_wrong_param = QLabel(f'Inform wrong param!')
        self.label_inform_wrong_param.setStyleSheet(style_label_successful)
        self.label_inform_wrong_param.setVisible(False)

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
        self.layout_chose_file.addWidget(self.label_select_file_to_convert)
        self.layout_chose_file.addLayout(self.layout_browse_file)
        self.layout_chose_file.addWidget(self.label_select_destination_file)
        self.layout_chose_file.addLayout(self.layout_browse_file_2)

        self.button_layout = QVBoxLayout()
        #self.button_layout.addWidget(self.button_to_cfg)
        #self.button_layout.addWidget(self.button_to_excel)
        self.button_layout.addWidget(self.label_to_many_files)
        self.button_layout.addWidget(self.label_wrong_file_type)
        self.button_layout.addWidget(self.label_no_file_to_convert)
        self.button_layout.addWidget(self.label_chose_correct_file)
        self.button_layout.addWidget(self.label_chose_correct_destination_file)

        self.line_edit_new_param = QLineEdit()
        self.line_edit_new_param.setStyleSheet(style_edit_line_browse_file)
        self.line_edit_new_param.setVisible(True)
        self.button_new_param = QPushButton('Apply')
        self.button_new_param.clicked.connect(self.get_new_param)
        self.button_new_param.setStyleSheet(style_button_search_file)
        self.button_new_param.setVisible(False)
        self.layout_new_param = QHBoxLayout()
        self.layout_new_param.addWidget(self.line_edit_new_param)
        self.layout_new_param.addWidget(self.button_new_param)

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
        #settings.line_edit_new_param.setVisible(True)
        self.main_window_layout.addLayout(self.layout_new_param)
        self.main_window_layout.addWidget(self.label_conversion_finished_failure)
        self.main_window_layout.addWidget(self.label_conversion_finished_successful)

        self.w = QWidget()
        self.w.setLayout(self.main_window_layout)
        self.setCentralWidget(self.w)



if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()




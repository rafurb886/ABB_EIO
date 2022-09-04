import os.path

from PyQt5.QtWidgets import QApplication, \
                            QLabel, \
                            QWidget, \
                            QMainWindow, \
                            QPushButton, \
                            QVBoxLayout, \
                            QHBoxLayout, \
                            QFileDialog, \
                            QLineEdit, \
                            QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDir, QObject, QThread, pyqtSignal, pyqtSlot
from EIOConverter import SignalsConverterToCfg, SignalsConverterToExcel
from errors import *
from app_qt_styles import *
import sys, time
import settings


available_extension = ['.cfg', '.xlsx']

class UserInterfaceToNewParams(QObject):
    show_edit_line = pyqtSignal()

    def run(self):
        print('jestem 1')
        while True:
            if settings.global_waiting_for_user_new_param:
                self.show_edit_line.emit()
                print('jestem 2')

                settings.global_waiting_for_user_new_param = False
            time.sleep(0.5)

class MainWindow(QMainWindow):
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

        self.thread = QThread()
        self.user_interface_to_new_param = UserInterfaceToNewParams()
        self.user_interface_to_new_param.moveToThread(self.thread)
        self.thread.started.connect(self.user_interface_to_new_param.run)
        self.user_interface_to_new_param.show_edit_line.connect(self.show_edit_line_to_new_param)
        self.thread.start()

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

    def browse_file_to_convert(self):
        self.file_path = QFileDialog.getOpenFileName(self, caption='Choose File',
                                                                directory=self.dir_path,
                                                                filter=self.filter_name)[0]
        if self.file_path != '':
            self.get_file_to_convert()

    def get_file_to_convert(self):
        self.reset_all_labels()
        try:
            self._file_name, self._file_extension = self.split_file_to_name_and_extension(self.file_path)
            self.check_browse_file(self.file_path)
            self.conversion_to = self.chose_conversation_type(self._file_extension)
            self.chose_destination_file()
        except ConverterError as e:
            self.file_path = ''
            print(e)
        self.lineEdit_browse_file.setText(self.file_path)

    def chose_conversation_type(self, file_extension):
        if file_extension == '.xlsx':
            return 'cfg'
        if file_extension == '.cfg':
            return 'xlsx'

    def split_file_to_name_and_extension(self, path):
        return os.path.splitext(path)

    def get_destination_file(self):
        self._destination_file_path = QFileDialog.getSaveFileName(self,
                                                                caption='Choose File',
                                                                directory=self.dir_path,
                                                                filter=self.filter_destination_name)[0]
        try:
            self._destination_name, self._destination_extension = self.split_file_to_name_and_extension(self._destination_file_path)
            self.check_browse_destination_file(self._destination_extension)
        except ConverterError as e:
            if self._destination_file_path != '':
                self.label_chose_correct_destination_file.setVisible(True)
        if self._destination_file_path != '':
            self.lineEdit_browse_file_2.setText(self._destination_file_path)

    def get_new_param(self):
        pass

    def check_browse_file(self, path):
        if not os.path.exists(path):
            self.label_chose_correct_file.setVisible(True)
            raise ConverterError('Condition: File no exist!!!')
        else:
            self.label_chose_correct_file.setVisible(False)

        file_name, file_extension = self.split_file_to_name_and_extension(path)
        if file_extension not in available_extension:
            self.label_wrong_file_type.setVisible(True)
            raise ConverterError('Condition: Wrong file type to edit!')
        else:
            self.label_wrong_file_type.setVisible(False)

    def check_browse_destination_file(self, file_extension):
        if file_extension not in available_extension or file_extension == self._file_extension:
            self.label_chose_correct_destination_file.setVisible(True)
            raise ConverterError('Condition: Wrong destination file!')
        else:
            self.label_chose_correct_destination_file.setVisible(False)

    def set_default_destination_file(self):
        self.directory_to_save = os.path.split(self.file_path)[0]
        temp_file_name = f'{self._file_name}_converted.{self._destination_file_extension[self.conversion_to]}'
        self._destination_file = os.path.join(self.directory_to_save, temp_file_name)
        file_iteration = 1
        while os.path.exists(self._destination_file):
            temp_file_name = f'{self._file_name}_converted_{file_iteration}.'\
                             f'{self._destination_file_extension[self.conversion_to]}'
            self._destination_file = os.path.join(self.directory_to_save, temp_file_name)
            file_iteration += 1
        return self._destination_file

    def chose_destination_file(self):
        self.lineEdit_browse_file_2.setText(self.set_default_destination_file())

    def reset_all_labels(self):
        self.label_chose_correct_file.setVisible(False)
        self.label_chose_correct_destination_file.setVisible(False)
        self.label_to_many_files.setVisible(False)
        self.label_wrong_file_type.setVisible(False)
        self.label_no_file_to_convert.setVisible(False)

    def msgbox_file_exist(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("I have a question!")
        dlg.setText("File exist. Do you want continue?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()

        if button == QMessageBox.No:
            raise ConverterError('Conversion: User stop.')

    def inform_user_conversion_finished(self):
        self.label_conversion_finished_successful.setVisible(True)

    def init_app_after_conversion(self):
        self.reset_all_labels()

    def show_edit_line_to_new_param(self):
        print('a tu jestem')
        self.line_edit_new_param.setVisible(True)
        return

    def convert_file(self):
        self.reset_all_labels()
        self.line_edit_new_param.setVisible(False)
        try:
            self.source_file = self.get_and_check_source_file()
            self.destination_file = self.get_and_check_destination_file()
            print(self.destination_file)

            if self.conversion_to == 'cfg':
                self.convert_obj = SignalsConverterToCfg.from_excel(self.source_file)
            elif self.conversion_to == 'xlsx':
                self.convert_obj = SignalsConverterToExcel.from_cfg(self.source_file)

            self.convert_obj.convert(self.destination_file)
            self.inform_user_conversion_finished()
            self.init_app_after_conversion()
        except ConverterError as e:
            print(f'Conversion stopped. {e}')
        except Exception as e:
            print(f'Conversion stopped. {e}')

    def get_and_check_source_file(self):
        temp_source_file = self.lineEdit_browse_file.text()
        try:
            self._file_name, self._file_extension = self.split_file_to_name_and_extension(temp_source_file)
            self.check_browse_file(temp_source_file)
            self.conversion_to = self.chose_conversation_type(self._file_extension)
        except ConverterError as e:
            temp_source_file = ''
            raise ConverterError(e)
        return temp_source_file

    def get_and_check_destination_file(self):
        temp_destination_file = self.lineEdit_browse_file_2.text()
        try:
            if not os.path.exists(os.path.dirname(temp_destination_file)):
                self.label_chose_correct_destination_file.setVisible(True)
                raise ConverterError('Conversion: Wrong file path.')
            if os.path.exists(temp_destination_file):
                self.msgbox_file_exist()
            self._destination_name, self._destination_extension = self.split_file_to_name_and_extension(temp_destination_file)
            self.check_browse_destination_file(self._destination_extension)
            return temp_destination_file
        except ConverterError as e:
            raise ConverterError(e)



if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()




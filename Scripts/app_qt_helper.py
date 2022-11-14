import os.path
from PyQt5.QtWidgets import QFileDialog, \
    QMessageBox
from PyQt5.QtCore import QThreadPool, QDir
from EIOConverter import SignalsConverterToCfg, SignalsConverterToExcel
from errors import *
from app_qt_threads import ThreadConversion
from app_qt_data import CFGConverterConstants

FILTER_SOURCE_NAME = 'All files (*.*)'
FILTER_DESTINATION_NAME = 'Files (*.cfg *.xlsx)'
DESTINATION_FILE_NAME = {'xlsx': 'converted_xlsx',
                         'cfg': 'converted_cfg'}
DESTINATION_FILE_EXTENSION = {'xlsx': 'xlsx',
                              'cfg': 'cfg'}
DEFAULT_DESTINATION_NAME = ''


class QtAppHelper:
    CONVERTER_CONST = CFGConverterConstants()

    def __init__(self, view, main_window):
        self.view = view
        self.dir_path = QDir.currentPath()
        self.main_window = main_window
        self.file_path = None
        self.conversion_to = ''
        self.destination_file = ''
        self._destination_file = ''
        self._destination_file_path = ''
        self._destination_extension = ''
        self._destination_name = ''
        self._file_name = ''
        self._file_extension = ''
        self.view.thread_to_conversion = None
        self.source_file = ''
        self.directory_to_save = ''

    def browse_file_to_convert(self):
        self.file_path = QFileDialog.getOpenFileName(self.main_window, caption='Choose File',
                                                          directory=QDir.currentPath(), filter=FILTER_SOURCE_NAME)[0]
        if self.file_path != '':
            self.get_file_to_convert()

    def get_file_to_convert(self):
        self.reset_all_labels()
        try:
            self._file_name, self._file_extension = self.split_file_to_name_and_extension(self.file_path)
            self.check_browse_file(self.file_path)
            self.conversion_to = self.chose_conversation_type(self._file_extension)
            self.chose_destination_file()
        except ApplicationError as e:
            self.file_path = ''
            self.show_application_error(e.args)
        self.view.lineEdit_browse_file.setText(self.file_path)

    def chose_conversation_type(self, file_extension):
        if file_extension == '.xlsx':
            return 'cfg'
        if file_extension == '.cfg':
            return 'xlsx'

    @staticmethod
    def split_file_to_name_and_extension(path):
        return os.path.splitext(path)

    def get_destination_file(self):
        self._destination_file_path = QFileDialog.getSaveFileName(self.main_window,
                                                                  caption='Choose File',
                                                                  directory=self.dir_path,
                                                                  filter=FILTER_DESTINATION_NAME)[0]
        try:
            self._destination_name, self._destination_extension = self.split_file_to_name_and_extension(
                self._destination_file_path)
            self.check_browse_destination_file(self._destination_extension)
        except ApplicationError as e:
            if self._destination_file_path != '':
                self.show_application_error(e.args)
                # self.view.label_chose_correct_destination_file.setVisible(True)
        if self._destination_file_path != '':
            self.view.lineEdit_browse_file_2.setText(self._destination_file_path)

    def check_browse_file(self, path):
        if not os.path.exists(path):
            # self.view.label_chose_correct_file.setVisible(True)
            raise ApplicationError('File no exist!!!')
        else:
            self.view.label_chose_correct_file.setVisible(False)

        file_name, file_extension = self.split_file_to_name_and_extension(path)
        if file_extension not in self.CONVERTER_CONST.AVAILABLE_EXTENSION:
            # self.view.label_wrong_file_type.setVisible(True)
            raise ApplicationError('Wrong file type to edit! Available {.cfg, .xlsx}')
        else:
            self.view.label_wrong_file_type.setVisible(False)

    def check_browse_destination_file(self, file_extension):
        if file_extension not in self.CONVERTER_CONST.AVAILABLE_EXTENSION or file_extension == self._file_extension:
            # self.view.label_chose_correct_destination_file.setVisible(True)
            raise ApplicationError('Wrong destination file!')
        else:
            self.view.label_chose_correct_destination_file.setVisible(False)

    def set_default_destination_file(self):
        self.directory_to_save = os.path.split(self.file_path)[0]
        temp_file_name = f'{self._file_name}_converted.{DESTINATION_FILE_EXTENSION[self.conversion_to]}'
        self._destination_file = os.path.join(self.directory_to_save, temp_file_name)
        file_iteration = 1
        while os.path.exists(self._destination_file):
            temp_file_name = f'{self._file_name}_converted_{file_iteration}.' \
                             f'{DESTINATION_FILE_EXTENSION[self.conversion_to]}'
            self._destination_file = os.path.join(self.directory_to_save, temp_file_name)
            file_iteration += 1
        return self._destination_file

    def chose_destination_file(self):
        self.view.lineEdit_browse_file_2.setText(self.set_default_destination_file())

    def reset_all_labels(self):
        self.view.label_chose_correct_file.setVisible(False)
        self.view.label_chose_correct_destination_file.setVisible(False)
        self.view.label_to_many_files.setVisible(False)
        self.view.label_wrong_file_type.setVisible(False)
        self.view.label_no_file_to_convert.setVisible(False)
        self.view.label_application_error.setVisible(False)

    def msgbox_file_exist(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("I have a question!")
        dlg.setText("File exist. Do you want continue?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()

        if button == QMessageBox.No:
            raise ApplicationError('User stop.')

    def inform_user_conversion_finished(self):
        self.view.label_conversion_finished_successful.setVisible(True)

    def init_app_after_conversion(self):
        self.reset_all_labels()

    def ask_user_correct_param(self, question_str):
        self.view.label_wrong_param.setVisible(True)
        self.view.label_info_wrong_param.setText(question_str)
        self.view.label_info_wrong_param.setVisible(True)
        self.view.line_edit_new_param.setVisible(True)
        self.view.button_new_param.setVisible(True)

    def get_new_param(self):
        user_new_param = self.view.line_edit_new_param.text()
        if user_new_param != '':
            self.thread_to_conversion.signals.set_user_new_param.emit(user_new_param)
        else:
            raise ApplicationError('New parameter is empty!')

    def create_conversion_thread(self):
        self.view.threadpool = QThreadPool()
        self.thread_to_conversion = ThreadConversion(main_window=self.main_window)
        self.thread_to_conversion.signals.question.connect(self.ask_user_correct_param)
        self.thread_to_conversion.signals.error_message.connect(self.show_conversion_error_message)
        self.thread_to_conversion.signals.finished.connect(self.show_successful_conversion)
        self.thread_to_conversion.signals.set_user_new_param.connect(self.thread_to_conversion.set_new_param)
        self.view.threadpool.start(self.thread_to_conversion)

    def show_conversion_error_message(self, error):
        self.view.label_wrong_param.setText(error)
        self.view.label_wrong_param.setVisible(True)

    def show_successful_conversion(self):
        self.view.label_conversion_finished.setVisible(True)

    def convert_file(self):
        self.reset_all_labels()
        try:
            self.source_file = self.get_and_check_source_file()
            self.destination_file = self.get_and_check_destination_file()
            print(f'MAIN TASK:{self.destination_file}')
            self.create_conversion_thread()
        except ConverterError as e:
            print(f'Conversion stopped. {e}')
        except ApplicationError as e:
            self.show_application_error(e.args)
        except Exception as e:
            print(f'Conversion stopped. {e}')

    def convert_file_old(self):
        self.reset_all_labels()
        try:
            self.source_file = self.get_and_check_source_file()
            self.destination_file = self.get_and_check_destination_file()

            if self.conversion_to == 'cfg':
                self.main_window.converted_obj = SignalsConverterToCfg.from_excel(self.source_file)
            elif self.conversion_to == 'xlsx':
                self.main_window.converted_obj = SignalsConverterToExcel.from_cfg(self.source_file)

            # self.create_and_start_thread_to_conversion()
            self.main_window.attach_views_to_model()
            self.main_window.converted_obj.convert(self.destination_file)
            print('CONVERSION DONE !!')
            self.inform_user_conversion_finished()
            self.init_app_after_conversion()
        except ConverterError as e:
            print(f'Conversion stopped. {e}')
        except Exception as e:
            print(f'Conversion stopped. {e}')

    def get_and_check_source_file(self):
        temp_source_file = self.view.lineEdit_browse_file.text()
        try:
            self._file_name, self._file_extension = self.split_file_to_name_and_extension(temp_source_file)
            self.check_browse_file(temp_source_file)
            self.conversion_to = self.chose_conversation_type(self._file_extension)
        except ApplicationError as e:
            raise ApplicationError(e)
        return temp_source_file

    def get_and_check_destination_file(self):
        temp_destination_file = self.view.lineEdit_browse_file_2.text()
        try:
            if not os.path.exists(os.path.dirname(temp_destination_file)):
                # self.view.label_chose_correct_destination_file.setVisible(True)
                raise ApplicationError('Wrong destination file path.')
            if os.path.exists(temp_destination_file):
                self.msgbox_file_exist()
            self._destination_name, self._destination_extension = self.split_file_to_name_and_extension(
                temp_destination_file)
            self.check_browse_destination_file(self._destination_extension)
            return temp_destination_file
        except ApplicationError as e:
            raise ApplicationError(e)

    def show_application_error(self, error):
        self.view.label_application_error.setText(str(*error))
        self.view.label_application_error.setVisible(True)

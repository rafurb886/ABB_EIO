import os.path
from PyQt5.QtWidgets import QFileDialog, \
                            QMessageBox
from EIOConverter import SignalsConverterToCfg, SignalsConverterToExcel
from errors import *
from app_qt_threads import *
from app_qt_data import *


class QtAppHelper:

    def __init__(self):
        pass

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
            self._destination_name, self._destination_extension = self.split_file_to_name_and_extension(
                self._destination_file_path)
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
            temp_file_name = f'{self._file_name}_converted_{file_iteration}.' \
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


    def create__and_start_thread_to_conversion(self):
        self.thread_conversion = QThread()
        self.user_interface_to_new_param = UserInterfaceToNewParams()
        self.user_interface_to_new_param.moveToThread(self.thread_conversion)
        self.thread_conversion.started.connect(self.user_interface_to_new_param.run)
        self.user_interface_to_new_param.show_edit_line.connect(self.show_edit_line_to_new_param)
        self.thread_conversion.start()


    def convert_file(self):
        self.reset_all_labels()
        self.create__and_start_thread_to_conversion()
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
            self._destination_name, self._destination_extension = self.split_file_to_name_and_extension(
                temp_destination_file)
            self.check_browse_destination_file(self._destination_extension)
            return temp_destination_file
        except ConverterError as e:
            raise ConverterError(e)

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



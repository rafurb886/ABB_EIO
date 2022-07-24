import os.path

from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, \
    QMainWindow, QPushButton, QAction, QMenu, QVBoxLayout, \
    QHBoxLayout, QGridLayout, QStackedLayout, QCheckBox, \
    QFileSystemModel, QTreeView, QFileDialog, QLineEdit
from PyQt5.QtCore import Qt, QSize, QDir
from EIOConverter import SignalsConverterToCfg, SignalsConverterToExcel
from errors import *
import sys


available_extension = ['.cfg', '.xlsx']
# COLORS IN RGB
color_background = 'Gainsboro'
color_background_label = f'Gainsboro'
color_background_button_hover = f'rgb(120, 120, 120)'
color_background_button = f'rgb(140, 140, 140)'
color_background_drag_and_drop = 'LightSlateGray'
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
style_button_search_file =      f"QPushButton {{background-color: {color_background_button};" \
                    f" color: {color_font_text};" \
                    f" font-size: 15px;" \
                    f" font: bold italic 'Times New Roman';" \
                    f" max-width: 300px;" \
                    f" text-align: center;" \
                    f" }}" \
                    f" QPushButton:hover {{"\
                    f" background-color: {color_background_button_hover};" \
                    f" color: {color_font_text}" \
                    f"}}"
style_button_convert = f"QPushButton {{background-color: {color_background_button};" \
                    f" color: Black;" \
                    f" font-size: 15px;" \
                    f" font: bold italic 'Times New Roman';" \
                    f" max-width: 300px;" \
                    f" text-align: center;" \
                    f" }}" \
                    f" QPushButton:hover {{"\
                    f" background-color: {color_background_button_hover};" \
                    f" color: Black" \
                    f"}}"
style_check_box =   f" QCheckBox {{"\
                    f" color: {color_font_text};" \
                    f" font-size: 25px;" \
                    f" font: bold italic 'Times New Roman';" \
                    f" max-width: 400px;" \
                    f" mix-width: 400px;" \
                    f" text-align: center;" \
                    f" padding :10px;" \
                    f" }}"

style_label_error =         f" QLabel {{"\
                            f" background-color: {color_background_label};" \
                            f" color: FireBrick;" \
                            f" font-size: 15px;" \
                            f" font: bold italic 'Times New Roman';" \
                            f" max-width: 400px;" \
                            f" qproperty-alignment: AlignCenter;"\
                            f" border: 2px solid FireBrick"\
                            f"}}"

style_drag_and_drop_label = f" QLabel {{"\
                            f" background-color: {color_background_drag_and_drop};" \
                            f" color: white;"\
                            f" font: bold italic 'Times New Roman';" \
                            f" border-radius: 5px;"\
                            f" max-width: 300px;" \
                            f" max-height: 300px;" \
                            f" qproperty-alignment: AlignCenter;"\
                            f"}}"

style_edit_line_browse_file = f" QLineEdit {{"\
                            f" background-color: white;" \
                            f" min-width: 300px;" \
                            f"}}"
style_select_file =         f" QLabel {{"\
                            f" background-color: {color_background_label};" \
                            f" color: Black;" \
                            f" font-size: 10px;" \
                            f" font: bold italic 'Times New Roman';" \
                            f" max-width: 400px;" \
                            f" qproperty-alignment: AlignLeft;"\
                            f" padding :1px;" \
                            f"}}"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        " normal application variable"
        self.file_path = None
        self.filter_name = 'All files (*.*)'
        self.filter_destination_name = 'Files (*.cfg *.xlsx)'
        self.dir_path = QDir.currentPath()
        self.destination_file = ''
        self.conversion_to = ''
        self._destination_file_name = {'xlsx': 'converted_xlsx',
                                       'cfg': 'converted_cfg'}
        self._destination_file_extension = {'xlsx': 'cfg',
                                            'cfg': 'xlsx'}
        self.default_destination_file = ''
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
        self.button_layout.addWidget(self.button_to_cfg)
        self.button_layout.addWidget(self.button_to_excel)
        self.button_layout.addWidget(self.label_to_many_files)
        self.button_layout.addWidget(self.label_wrong_file_type)
        self.button_layout.addWidget(self.label_no_file_to_convert)
        self.button_layout.addWidget(self.label_chose_correct_file)
        self.button_layout.addWidget(self.label_chose_correct_destination_file)

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
            self.get_file_to_concert()

    def browse_file_to_convert(self):
        self.file_path = QFileDialog.getOpenFileName(self, caption='Choose File',
                                                                directory=self.dir_path,
                                                                filter=self.filter_name)[0]
        self.get_file_to_concert()

    def get_file_to_concert(self):
        try:
            self.check_browse_file()
            self.chose_conversation_type()
            self.chose_destination_file_if_field_is_empty()
        except WrongFile as e:
            self.label_wrong_file_type.setVisible(True)
            self.file_path = ''
            print(e)
        self.lineEdit_browse_file.setText(self.file_path)

    def chose_conversation_type(self):
        if self._file_extension == '.xlsx':
            self.button_to_excel.setChecked(True)
            self.button_to_cfg.setChecked(False)
            self.conversion_to = 'xlsx'
        if self._file_extension == '.cfg':
            self.button_to_cfg.setChecked(True)
            self.button_to_excel.setChecked(False)
            self.conversion_to = 'cfg'

    def get_destination_file(self):
        self._destination_file_path = QFileDialog.getSaveFileName(self,
                                                                caption='Choose File',
                                                                directory=self.dir_path,
                                                                filter=self.filter_destination_name)[0]
        try:
            self.check_browse_destination_file()
        except WrongFile as e:
            self.label_chose_correct_destination_file.setVisible(True)
            self._destination_file_path = ''
            print(e)
        self.lineEdit_browse_file_2.setText(self._destination_file_path)

    def check_browse_file(self):
        self._file_name, self._file_extension = os.path.splitext(self.file_path)
        if self._file_extension not in available_extension:
            raise WrongFile('Wrong file to edit!')
        else:
            self.label_wrong_file_type.setVisible(False)
        print(f'File pah: {self.file_path}')


    def check_browse_destination_file(self):
        self._destination_file_name, self._destination_file_extension = os.path.splitext(self._destination_file_path)
        if self._destination_file_extension not in available_extension:
            raise WrongFile('Wrong destination file!')
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

    def chose_destination_file_if_field_is_empty(self):
        if self.lineEdit_browse_file_2.text() == '':
            self.lineEdit_browse_file_2.setText(self.set_default_destination_file())





    def convert_file(self):
        self.destination_file = self.set_and_check_destination_file()
        if self.destination_file == '':
            return
        if self.conversion_to == 'xlsx':
            self.convert_obj = SignalsConverterToCfg.from_excel(self.destination_file)
        elif self.conversion_to == 'cfg':
            self.convert_obj = SignalsConverterToExcel.from_cfg(self.destination_file)
        self.convert_obj.convert(self.destination_file)

    def set_and_check_destination_file(self):
        temp_destination_file = self.lineEdit_browse_file_2.text()
        if os.path.exists(os.path.dirname(temp_destination_file)):
            if not os.path.exists(temp_destination_file):
                print('do it')
            else:
                print('plik już istnieje, chcesz go nadpisać?')
        else:
            print('nie ma takiej ścieżki')




if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()




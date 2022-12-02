import regex as re
import pandas as pd
import numpy as np
import time
from PyQt5.QtCore import QObject
from .errors import ConverterError
from .helper import *
from .app_qt_data import CFGConverterConstants
from . import settings

class ValidateSignalsCellsInLine:
    CONST = CFGConverterConstants()

    def __init__(self, line, converter=None):
        self.line = line
        self.converter = converter

    def check_all_cells_valid(self):
        self.line = self.check_correct_character_in_columns(self.CONST.REGEX_FOR_USER_NAMES.keys())
        self.line = self.check_correct_parameters_in_columns(self.CONST.AVAILABLE_SIGNALS_PARAM.keys())
        #self.line = self.check_default_column()
        return self.line

    def check_correct_character_in_columns(self, columns_name):
        for column in columns_name:
            correct_length = self.check_length_of_name(self.line[column], column)
            correct_character = self.check_correct_character(self.line[column],
                                                             regex_str=self.CONST.REGEX_FOR_USER_NAMES[column],
                                                             available_null=self.CONST.AVAILABLE_NULL_NAME[column],
                                                             default_null_value=self.CONST.DEFAULT_VALUE_FOR_COLUMNS[column])
            if correct_length and correct_character:
                continue
            if settings.global_qt_app_run:
                self.line[column] = self.get_user_param_in_qt_app(column)
            else:
                self.line[column] = self.get_user_param_in_terminal(column)
            self.check_correct_character_in_columns([column])
        return self.line

    def check_correct_parameters_in_columns(self, columns_name):
        for column in columns_name:
            if self.line[column] in self.CONST.AVAILABLE_SIGNALS_PARAM[column] \
                    or (self.CONST.AVAILABLE_NULL_NAME[column] and self.line[column] == self.CONST.DEFAULT_VALUE_FOR_COLUMNS[column]):
                continue
            if settings.global_qt_app_run:
                self.line[column] = self.get_user_param_in_qt_app(column)
            else:
                self.line[column] = self.get_user_param_in_terminal(column)
            self.check_correct_parameters_in_columns([column])
        return self.line

    def check_length_of_name(self, string, column):
        return len(string) < self.CONST.MAX_LENGTH_OF_NAME if column != 'Label' else True

    @staticmethod
    def check_correct_character(string_to_check, regex_str=r'[_a-zA-Z0-9]+',
                                available_null=False, default_null_value=np.NaN):
        if available_null and string_to_check == default_null_value:
            return True
        pattern = re.compile(regex_str)
        return pattern.fullmatch(string_to_check)

    def set_question_string(self, column):
        question_str = self.add_additional_hints_to_question(column)
        question_str = question_str + '\n' + f'Wrong {column}: {self.line[column]} in signal {self.line["Name"]}.' \
                                             f'\nEnter correct {column}: '
        return question_str

    def add_additional_hints_to_question(self, column):
        question_str = ''
        if not self.check_length_of_name(self.line[column], column):
            question_str = question_str + 'Too long name!!! \n'
        return question_str

    def get_user_param_in_qt_app(self, column):
        question_str = self.set_question_string(column)
        self.converter.signals.question.emit(question_str)
        self.converter.is_paused = True
        while self.converter.is_paused:
            time.sleep(0.1)
            if self.converter.is_killed:
                break  # do poprawy
        print(self.converter.user_new_param)
        return self.converter.user_new_param

    def get_user_param_in_terminal(self, column):
        return input(self.set_question_string(column))

    def check_is_digit(self, column_name):
        for column in column_name:
            if isinstance(self.line[column], float) or isinstance(self.line[column], int):
                continue
            self.line[column] = input(f'{column} in signal {self.line["Name"]} is not a digit. '
                                      f'Current value: {self.line[column]}\n Enter correct value: ')
            self.check_is_digit([column])
        self.line[column_name] = self.line[column_name].astype('float')
        return self.line

    def check_default_column(self, column='Default'):
        #TODO: add it to checking
        if isinstance(self.line[column], float) or isinstance(self.line[column], int):
            if self.line['SignalType'] in ['DI', 'DO'] and self.line[column] in [0, 1] \
                    or self.line['SignalType'] in ['GI', 'GO'] and self.line[column] % 1 == 0 \
                    or self.line['SignalType'] in ['AI', 'AO'] and isinstance(self.line[column], float) \
                    or pd.isna(self.line[column]):
                return self.line

        self.line[column] = input(
            f'Default value in signal {self.line["Name"]} is not valid. Current value: {self.line["Default"]} in signal type {self.line["SignalType"]} \n Enter correct value: ')
        self.check_default_column()
        return self.line


class SignalsConverterToCfg(QObject):
    CONST = CFGConverterConstants()

    def __init__(self, data=None, signal_show_edit_line_to_new_param= None):
        '''
        Args:
            data: pandas object containing all data to convert
        '''
        super().__init__()
        self.data = data
        self.text_to_write = ''
        self.is_paused = False
        self.is_killed = False


    @classmethod
    def from_excel(cls, source_path):
        '''
        name of columns:'Name', 'SignalType', 'Device', 'Label', 'DeviceMap', 'Category',
                        'Access', 'Default', 'SafeLevel', 'EncType', 'MaxLog', 'MaxPhys',
                        'MaxPhysLimit', 'MaxBitVal', 'MinLog', 'MinPhys', 'MinPhysLimit', 'MinBitVal'
        Args:
            path: path to excel file, which contain 'INPUT' and 'OUTPUT' sheets and have correct structure
            source_path: absolute source path
        Returns: object from class
        '''
        excel_file = pd.ExcelFile(source_path)
        df_input = pd.read_excel(excel_file, sheet_name='INPUT')
        df_output = pd.read_excel(excel_file, sheet_name='OUTPUT')
        df_all = pd.concat([df_input, df_output], ignore_index=True)

        if not check_uniqe_val_in_column(df_all, 'Name'):
            raise ConverterError('Names are NOT unique!')
        df_all = drop_column_if_exist(df_all, ['Unnamed: 0', 'DeviceMapToSort'])
        df_all = df_remove_other_column(df_all, cls.CONST.COLUMNS_NAME)
        df_all = add_column_if_no_exist(df_all, cls.CONST.COLUMNS_NAME, cls.CONST.DEFAULT_VALUE_FOR_COLUMNS)
        df_all = sort_columns(df_all, cls.CONST.COLUMNS_NAME)
        df_all.reset_index()
        return cls(df_all)

    def set_type_for_columns(self, columns: list = None, type_of_column: str = None):
        for column in columns:
            self.data[column] = self.data[column].astype(type_of_column)

    def strip_columns(self, columns):
        for column in columns:
            self.data[column] = self.data[column].str.strip()

    def set_str_to_uppercase(self, columns):
        for column in columns:
            self.data[column] = self.data[column].str.upper()  # apply(lambda x: 'NAN' if x == 'nan' else x)

    def set_nan_str_to_uppercase(self, columns):
        for column in columns:
            self.data[column] = 'NAN' if self.data[column].str == 'nan' else self.data[column]

    def check_all_cells(self):
        self.data = self.data.apply(lambda line: (ValidateSignalsCellsInLine(line, self).check_all_cells_valid()), axis=1)

    def write_signals_to_cfg(self, path):
        self.text_to_write = self.data.apply(self.generate_signal_text, axis=1)
        print(self.text_to_write)
        with open(path, 'w') as file:
            file.writelines(self.text_to_write)

    def generate_signal_text(self, line):
        result_string = ''
        for column in self.CONST.COLUMNS_NAME:
            if not pd.isnull(line[column]):
                if column in self.CONST.WITH_APOSTROPHE:
                    try:
                        if line[column].upper() not in ['NAN']:
                            result_string += f'-{column} "{line[column]}"\\\n'
                    except Exception as e:
                        raise ConverterError('Error during generating file!')
                if column in self.CONST.WITHOUT_APOSTROPHE:
                    result_string += f'-{column}{line[column]}\\\n'
        return result_string[:-2] + '\n' * 2

    def convert(self, destination_file):
        print('CONVERTER: Conversion to cfg started')
        self.set_type_for_columns(['Label', 'Category', 'Access', 'SafeLevel', 'EncType'], 'str')
        self.strip_columns(['SignalType', 'Access', 'SafeLevel', 'EncType'])

        self.set_str_to_uppercase(['Category', 'Access', 'SafeLevel', 'EncType'])
        self.set_nan_str_to_uppercase(['Label'])
        self.check_all_cells()
        print('done')
        self.write_signals_to_cfg(destination_file)
        #print(self.data)
        print('done')


class SignalsConverterToExcel(QObject):
    CONST = CFGConverterConstants()

    def __init__(self, data=None, source_path=None):
        '''
        Args:
            data: pandas data frame
        '''
        super().__init__()
        self.data = data
        self.path_to_cfg = source_path
        self.df_input = None
        self.df_output = None

    @classmethod
    def find_params(cls, string_line, columns_name):
        result_dict = dict()
        result = None
        for column in columns_name:
            if column in cls.CONST.WITH_APOSTROPHE:
                pattern = re.compile(f'-{column} "(.*?)"')
            else:
                pattern = re.compile(f'-{column} (\d*)')
            result = pattern.search(string_line)
            if result is None:
                result_dict[column] = np.NaN
            else:
                result_dict[column] = result.group(1) #if result is None else np.NaN
        return result_dict

    @classmethod
    def find_signals_description(cls, file_data):
        pattern = re.compile(cls.CONST.REGEX_FOR_FIND_START_OF_SIGNAL_DESCRIPTION, re.DOTALL)
        match = pattern.search(file_data)
        return match.group(1)

    @classmethod
    def prepare_data_from_file(cls, file_data):
        file_data = file_data.replace('\\', '')
        roi = cls.find_signals_description(file_data)
        roi = roi.split('-Name')
        roi = list(map(lambda x: '-Name' + x, roi[1:]))
        return [line.replace('\n', '') for line in roi]

    @classmethod
    def from_cfg(cls, path):
        with open(r'H:\PythonProjects\ABB_EIO_translation\files\EIO_test.cfg', 'r') as file:
            file_data = file.read()
        roi = cls.prepare_data_from_file(file_data)
        df = pd.DataFrame(data=None, columns=cls.CONST.COLUMNS_NAME)
        for line_to_df in roi:
            to_df = pd.DataFrame(cls.find_params(line_to_df, cls.CONST.COLUMNS_NAME), index=[0])
            df = pd.concat([df, to_df], ignore_index=True)
        return cls(df, path)

    def _find_device_mapping_to_sort(self, df_line):
        pattern = re.compile(self.CONST.REGEX_FOR_SORTING_BY_DEVICE_MAP)
        result = pattern.search(df_line)
        return result.group(1)

    def _sort_df_by_device_map(self, df):
        # TODO: add sorting by device
        df['DeviceMapToSort'] = df['DeviceMap'].apply(self._find_device_mapping_to_sort)
        df['DeviceMapToSort'] = df['DeviceMapToSort'].astype('int32')
        return df.sort_values(by='DeviceMapToSort')

    def sort_data_frame(self):
        self.data = self._sort_df_by_device_map(self.data)

    def _prepare_to_write(self):
        flt_input = self.data.SignalType.isin(self.CONST.INPUT_LABELS)
        flt_output = self.data.SignalType.isin(self.CONST.OUTPUT_LABELS)
        self.df_input = self.data[flt_input]
        self.df_output = self.data[flt_output]

    def write_to_excel(self, path):
        self._prepare_to_write()
        with pd.ExcelWriter(path) as writer:
            self.df_input.to_excel(writer, 'INPUT')
            self.df_output.to_excel(writer, 'OUTPUT')

    def convert(self, destination_file):
        self.sort_data_frame()
        self.write_to_excel(destination_file)
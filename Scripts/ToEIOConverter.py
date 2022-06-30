import regex as re
import pandas as pd
import numpy as np
from helper import *

import itertools

class DataRequirementsToConvertSignals:
    columns_name = ['Name', 'SignalType', 'Device', 'Label', 'DeviceMap', 'Category', 'Access', 'Default', 'SafeLevel',
                    'EncType', 'MaxLog', 'MaxPhys', 'MaxPhysLimit', 'MaxBitVal', 'MinLog', 'MinPhys', 'MinPhysLimit',
                    'MinBitVal']
    with_apostrophe = ['Name', 'SignalType', 'Device', 'Label', 'DeviceMap', 'Category', 'Access', 'SafeLevel',
                       'EncType']
    without_apostrophe = set(columns_name).difference(set(with_apostrophe))
    default_value_for_columns = {'Name': 'NAN',         'SignalType': 'NAN',    'Device': 'NAN',
                                 'Label': 'NAN',        'DeviceMap': 'NAN',     'Category': 'NAN',
                                 'Access': 'NAN',       'Default': np.NaN,      'SafeLevel': 'NAN',
                                 'EncType': 'NAN',      'MaxLog': np.NaN,      'MaxPhys': np.NaN,
                                 'MaxPhysLimit': np.NaN,'MaxBitVal': np.NaN,    'MinLog': np.NaN,
                                 'MinPhys': np.NaN,     'MinPhysLimit': np.NaN, 'MinBitVal': np.NaN}
    available_null_name =  {'Name': False,          'SignalType': False,    'Device': False,
                            'Label': True,          'DeviceMap': False,     'Category': True,
                            'Access': True,         'Default': True,        'SafeLevel': True,
                            'EncType': True,        'MaxLog': True,         'MaxPhys': True,
                            'MaxPhysLimit': True,   'MaxBitVal': True,      'MinLog': True,
                            'MinPhys': True,        'MinPhysLimit': True,   'MinBitVal': True}
    available_signals_param = { 'SignalType':   ['AI', 'AO', 'DI', 'DO', 'GI', 'GO'],
                                'SafeLevel':    ['SAFETYSAFELEVEL'], # usuniete NANy
                                'Access':       ['READONLY'],
                                'EncType':      ['UNSIGNED', 'SIGNED']}

    regex_for_mapping = r'(\d{1,4})(-\d{1,4})?'
    regex_for_label = r'[\w _]+'
    regex_for_names = r'[a-zA-Z][_a-zA-Z0-9]+'
    regex_for_user_names = {'Name': regex_for_names,        'Device': regex_for_names,      'Label': regex_for_label,
                            'DeviceMap': regex_for_mapping, 'Category': regex_for_names}


class ValidateSignalsCellsInLine(DataRequirementsToConvertSignals):

    def __init__(self, line):
        self.line = line

    def check_all_cells_valid(self):
        self.line = self.check_correct_character_in_columns(self.regex_for_user_names.keys())
        self.line = self.check_correct_parameters_in_columns(self.available_signals_param.keys())
        return self.line

    @staticmethod
    def check_correct_character(string_to_check, regex_str=r'[_a-zA-Z0-9]+', available_null=False, default_null_value=np.NaN):
        if available_null and string_to_check == default_null_value:
            return True
        pattern = re.compile(regex_str)
        return pattern.fullmatch(string_to_check)

    def check_correct_character_in_columns(self, columns_name):
        for column in columns_name:
            if self.check_correct_character(self.line[column],
                                            regex_str=self.regex_for_user_names[column],
                                            available_null=self.available_null_name[column],
                                            default_null_value=self.default_value_for_columns[column]):
                continue
            self.line[column] = input(f'Wrong {column}: {self.line[column]} in signal {self.line["Name"]}.'
                                      f'\nEnter correct {column}: ')
            self.check_correct_character_in_columns([column])
        return self.line

    def check_correct_parameters_in_columns(self, columns_name):
        for column in columns_name:
            if self.line[column] in self.available_signals_param[column] \
                    or (self.available_null_name[column] and self.line[column] == self.default_value_for_columns[column]):
                continue
            self.line[column] = input(f'Wrong {column}: {self.line[column]} in signal {self.line["Name"]}. \n'
                                      f'Enter correct {column}: ')
            self.check_correct_parameters_in_columns([column])
        return self.line

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
        if isinstance(self.line[column], float) or isinstance(self.line[column], int):
            if self.line['SignalType'] in ['DI', 'DO'] and self.line[column] in [0, 1] \
                    or self.line['SignalType'] in ['GI', 'GO'] and self.line[column] % 1 == 0\
                    or self.line['SignalType'] in ['AI', 'AO'] and isinstance(self.line[column], float)\
                    or pd.isna(self.line[column]):
                return self.line

        self.line[column] = input(f'Default value in signal {self.line["Name"]} is not valid. Current value: {self.line["Default"]} in signal type {self.line["SignalType"]} \n Enter correct value: ')
        self.check_default_column()
        return self.line


class SignalsConverter(DataRequirementsToConvertSignals): # nie wiem czy dodać dziedziczenie z ValidateSignalsCellsInLine

    def __init__(self, data):
        '''
        Args:
            data: pandas object containing all data to convert
        '''
        self.data = data

    @classmethod
    def from_excel(cls, path):
        '''
        name of columns:'Name', 'SignalType', 'Device', 'Label', 'DeviceMap', 'Category',
                        'Access', 'Default', 'SafeLevel', 'EncType', 'MaxLog', 'MaxPhys',
                        'MaxPhysLimit', 'MaxBitVal', 'MinLog', 'MinPhys', 'MinPhysLimit', 'MinBitVal'
        Args:
            path: path to excel file, which contain 'INPUT' and 'OUTPUT' sheets and have correct structure

        Returns: object from class
        '''
        excel_file = pd.ExcelFile(path)
        df_input = pd.read_excel(excel_file, sheet_name='INPUT')
        df_output = pd.read_excel(excel_file, sheet_name='OUTPUT')
        df_all = pd.concat([df_input, df_output], ignore_index=True)

        if not check_uniqe_val_in_column(df_all, 'Name'):
            raise Exception('Names are NOT unique')
        df_all = drop_column_if_exist(df_all, ['Unnamed: 0', 'DeviceMapToSort'])
        df_all = df_remove_other_column(df_all, cls.columns_name)
        df_all = add_column_if_no_exist(df_all, cls.columns_name, cls.default_value_for_columns)
        df_all = sort_columns(df_all, cls.columns_name)
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
            self.data[column] = self.data[column].str.upper()#apply(lambda x: 'NAN' if x == 'nan' else x)

    def set_nan_str_to_uppercase(self, columns):
        for column in columns:
            self.data[column] = 'NAN' if self.data[column].str == 'nan' else self.data[column]

    def check_all_cells(self):
        self.data = self.data.apply(lambda line: (ValidateSignalsCellsInLine(line).check_all_cells_valid()), axis=1)

    # mozliwe ze do zmiany na staticmethod bo zle argumenty
    def write_signal_to_cfg(self, line):
        result_string = ''
        for column in self.columns_name:
            if not pd.isnull(line[column]):
                if column in self.with_apostrophe:
                    try:
                        if line[column].upper() not in ['NAN']:
                            result_string += f'-{column} "{line[column]}"\\\n'
                    except:
                        pass
                if column in self.without_apostrophe:
                    result_string += f'-{column}{line[column]}\\\n'
        return result_string[:-2] + '\n' * 2











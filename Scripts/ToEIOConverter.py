import regex as re
import pandas as pd
import numpy as np
import itertools
from helper import check_uniqe_val_in_column, drop_column_if_exist, add_column_if_no_exist, df_remove_other_column

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

    available_signal_type = ['AI', 'AO', 'DI', 'DO', 'GI', 'GO']
    available_signal_safe_level = ['SAFETYSAFELEVEL', 'NAN']
    available_signal_access = ['READONLY', 'NAN']
    available_signal_enctype = ['UNSIGNED', 'SIGNED', 'NAN']

    regex_for_mapping = r'(\d{1,4})(-\d{1,4})?'
    regex_for_label = r'[\w _]+'
    regex_for_names = r'[_a-zA-Z0-9]+'
    regex_for_user_names = {'Name': regex_for_names,        'Device': regex_for_names,    'Label': regex_for_label,
                            'DeviceMap': regex_for_mapping, 'Category': regex_for_names}


class ValidateSignalsCellsInLine(DataRequirementsToConvertSignals):

    def __init__(self, line):
        self.line = line

    def check_all_cells_valid(self):
        self.line = self.check_correct_character_in_columns(['Name', 'DeviceMap'])
        return self.line

    def check_correct_character(self, string_to_check, regex_str=r'[_a-zA-Z0-9]+', available_null=False):
        if not available_null:  # dodac nulla
            pattern = re.compile(regex_str)
            return pattern.fullmatch(string_to_check)

    def check_correct_character_in_columns(self, columns_name):
        for column in columns_name:
            if self.check_correct_character(self.line[column], regex_str=self.regex_for_user_names[column]):
                return self.line
            self.line[column] = input(f'Wrong {column}: {self.line[column]}. \nEnter correct {column}: ')
            return self.check_correct_character_in_columns([column])



class SignalsConverter(ValidateSignalsCellsInLine):

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
        df_all.reset_index()
        return cls(df_all)

    def set_type_for_columns(self, columns: list = None, type_of_column: str = None):
        self.data[columns].astype(type_of_column)

    def set_uppercase_nan_if_empty_to_columns(self, columns):
        for column in columns:
            self.data[column] = self.data[column].apply(lambda x: 'NAN' if x == 'nan' else x)

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











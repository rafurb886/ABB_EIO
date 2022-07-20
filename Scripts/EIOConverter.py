import regex as re
import pandas as pd
import numpy as np
from helper import *


class DataRequirementsToConvertSignals:
    columns_name = ['Name', 'SignalType', 'Device', 'Label', 'DeviceMap', 'Category', 'Access', 'Default', 'SafeLevel',
                    'EncType', 'MaxLog', 'MaxPhys', 'MaxPhysLimit', 'MaxBitVal', 'MinLog', 'MinPhys', 'MinPhysLimit',
                    'MinBitVal']
    with_apostrophe = ['Name', 'SignalType', 'Device', 'Label', 'DeviceMap', 'Category', 'Access', 'SafeLevel',
                       'EncType']
    without_apostrophe = set(columns_name).difference(set(with_apostrophe))
    default_value_for_columns = {'Name': 'NAN', 'SignalType': 'NAN', 'Device': 'NAN',
                                 'Label': 'NAN', 'DeviceMap': 'NAN', 'Category': 'NAN',
                                 'Access': 'NAN', 'Default': np.NaN, 'SafeLevel': 'NAN',
                                 'EncType': 'NAN', 'MaxLog': np.NaN, 'MaxPhys': np.NaN,
                                 'MaxPhysLimit': np.NaN, 'MaxBitVal': np.NaN, 'MinLog': np.NaN,
                                 'MinPhys': np.NaN, 'MinPhysLimit': np.NaN, 'MinBitVal': np.NaN}
    available_null_name = {'Name': False, 'SignalType': False, 'Device': False,
                           'Label': True, 'DeviceMap': False, 'Category': True,
                           'Access': True, 'Default': True, 'SafeLevel': True,
                           'EncType': True, 'MaxLog': True, 'MaxPhys': True,
                           'MaxPhysLimit': True, 'MaxBitVal': True, 'MinLog': True,
                           'MinPhys': True, 'MinPhysLimit': True, 'MinBitVal': True}
    available_signals_param = {'SignalType': ['AI', 'AO', 'DI', 'DO', 'GI', 'GO'],
                               'SafeLevel': ['SAFETYSAFELEVEL'],  # usuniete NANy
                               'Access': ['READONLY'],
                               'EncType': ['UNSIGNED', 'SIGNED']}

    input_labels = ['DI', 'AI', 'GI']
    output_labels = ['DO', 'AO', 'GO']

    regex_for_mapping = r'(\d{1,4})(-\d{1,4})?'
    regex_for_label = r'[\w _]+'
    regex_for_names = r'[a-zA-Z][_a-zA-Z0-9]+'
    regex_for_sorting_by_device_map = '(\d+).?'
    regex_for_find_start_of_signal_description = r'EIO_SIGNAL:(.*)'
    regex_for_user_names = {'Name': regex_for_names, 'Device': regex_for_names, 'Label': regex_for_label,
                            'DeviceMap': regex_for_mapping, 'Category': regex_for_names}


class ValidateSignalsCellsInLine(DataRequirementsToConvertSignals):

    def __init__(self, line):
        self.line = line

    def check_all_cells_valid(self):
        self.line = self.check_correct_character_in_columns(self.regex_for_user_names.keys())
        self.line = self.check_correct_parameters_in_columns(self.available_signals_param.keys())
        return self.line

    @staticmethod
    def check_correct_character(string_to_check, regex_str=r'[_a-zA-Z0-9]+', available_null=False,
                                default_null_value=np.NaN):
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
                    or (
                    self.available_null_name[column] and self.line[column] == self.default_value_for_columns[column]):
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
                    or self.line['SignalType'] in ['GI', 'GO'] and self.line[column] % 1 == 0 \
                    or self.line['SignalType'] in ['AI', 'AO'] and isinstance(self.line[column], float) \
                    or pd.isna(self.line[column]):
                return self.line

        self.line[column] = input(
            f'Default value in signal {self.line["Name"]} is not valid. Current value: {self.line["Default"]} in signal type {self.line["SignalType"]} \n Enter correct value: ')
        self.check_default_column()
        return self.line


class SignalsConverterToCfg(DataRequirementsToConvertSignals):  # nie wiem czy dodać dziedziczenie z ValidateSignalsCellsInLine

    def __init__(self, data):
        '''
        Args:
            data: pandas object containing all data to convert
        '''
        self.data = data
        self.text_to_write = ''

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
            self.data[column] = self.data[column].str.upper()  # apply(lambda x: 'NAN' if x == 'nan' else x)

    def set_nan_str_to_uppercase(self, columns):
        for column in columns:
            self.data[column] = 'NAN' if self.data[column].str == 'nan' else self.data[column]

    def check_all_cells(self):
        self.data = self.data.apply(lambda line: (ValidateSignalsCellsInLine(line).check_all_cells_valid()), axis=1)

    def write_signals_to_cfg(self, path):
        self.text_to_write = self.data.apply(self.generate_signal_text, axis=1)
        print(self.text_to_write)
        with open(path, 'w') as file:
            file.writelines(self.text_to_write)

    def generate_signal_text(self, line):
        result_string = ''
        for column in self.columns_name:
            if not pd.isnull(line[column]):
                if column in self.with_apostrophe:
                    try:
                        if line[column].upper() not in ['NAN']:
                            result_string += f'-{column} "{line[column]}"\\\n'
                    except Exception as e:
                        print(f'Error during generating signal text: {e}')
                if column in self.without_apostrophe:
                    result_string += f'-{column}{line[column]}\\\n'
        return result_string[:-2] + '\n' * 2

    def convert(self, destination_file):
        self.set_type_for_columns(['Label', 'Category', 'Access', 'SafeLevel', 'EncType'], 'str')
        self.strip_columns(['SignalType', 'Access', 'SafeLevel', 'EncType'])
        self.set_str_to_uppercase(['Category', 'Access', 'SafeLevel', 'EncType'])
        self.set_nan_str_to_uppercase(['Label'])
        self.check_all_cells()
        self.write_signals_to_cfg(destination_file)
        print(self.data)


class SignalsConverterToExcel(DataRequirementsToConvertSignals):

    def __init__(self, data, path_to_cfg):
        '''
        Args:
            data: pandas data frame
        '''
        self.data = data
        self.path_to_cfg = path_to_cfg
        self.df_input = None
        self.df_output = None

    @classmethod
    def find_params(cls, string_line, columns_name):
        result_dict = dict()
        result = None
        for column in columns_name:
            if column in cls.with_apostrophe:
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
        pattern = re.compile(cls.regex_for_find_start_of_signal_description, re.DOTALL)
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
        df = pd.DataFrame(data=None, columns=cls.columns_name)
        for line_to_df in roi:
            to_df = pd.DataFrame(cls.find_params(line_to_df, cls.columns_name), index=[0])
            df = pd.concat([df, to_df], ignore_index=True)
        return cls(df, path)

    def _find_device_mapping_to_sort(self, df_line):
        pattern = re.compile(self.regex_for_sorting_by_device_map)
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
        flt_input = self.data.SignalType.isin(self.input_labels)
        flt_output = self.data.SignalType.isin(self.output_labels)
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

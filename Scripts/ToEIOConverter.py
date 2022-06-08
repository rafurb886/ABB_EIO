import regex as re
import pandas as pd
import numpy as np
import itertools
from helper import check_uniqe_val_in_column, drop_column_if_exist


class DataRequirementsToConvertSignals:
    columns_name = ['Name', 'SignalType', 'Device', 'Label', 'DeviceMap', 'Category', 'Access', 'Default', 'SafeLevel',
                    'EncType', 'MaxLog', 'MaxPhys', 'MaxPhysLimit', 'MaxBitVal', 'MinLog', 'MinPhys', 'MinPhysLimit',
                    'MinBitVal']
    with_apostrophe = ['Name', 'SignalType', 'Device', 'Label', 'DeviceMap', 'Category', 'Access', 'SafeLevel',
                       'EncType']
    without_apostrophe = set(columns_name).difference(set(with_apostrophe))

    available_signal_type = ['AI', 'AO', 'DI', 'DO', 'GI', 'GO']
    available_signal_safe_level = ['SAFETYSAFELEVEL', 'NAN']
    available_signal_access = ['READONLY', 'NAN']
    available_signal_enctype = ['UNSIGNED', 'SIGNED', 'NAN']

    regex_for_mapping = r'(\d{1,4})(-\d{1,4})?'
    regex_for_label = r'[\w _]+'
    regex_for_names = r'[_a-zA-Z0-9]+'


class SignalsConverter(DataRequirementsToConvertSignals):

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
        df_all = df_input.append(df_output)

        if not check_uniqe_val_in_column(df_all, 'Name'):
            raise Exception('Names are NOT unique')
        df_all.set_index('Name')
        df_all = drop_column_if_exist(df_all, ['Unnamed: 0', 'DeviceMapToSort'])
        df_all.reset_index()
        return cls(df_all)











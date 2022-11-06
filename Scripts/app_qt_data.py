import numpy as np


available_extension = ['.cfg', '.xlsx']

filter_name = 'All files (*.*)'
filter_destination_name = 'Files (*.cfg *.xlsx)'

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

max_length_of_name = 32
regex_for_mapping = r'(\d{1,4})(-\d{1,4})?'
regex_for_label = r'[\w _]+'
regex_for_names = r'[a-zA-Z][_a-zA-Z0-9]+'
regex_for_sorting_by_device_map = '(\d+).?'
regex_for_find_start_of_signal_description = r'EIO_SIGNAL:(.*)'
regex_for_user_names = {'Name': regex_for_names, 'Device': regex_for_names, 'Label': regex_for_label,
                        'DeviceMap': regex_for_mapping, 'Category': regex_for_names}

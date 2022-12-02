import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class CFGConverterConstants:

    __slots__ = ()
    AVAILABLE_EXTENSION = ['.cfg', '.xlsx']

    COLUMNS_NAME = ['Name', 'SignalType', 'Device', 'Label', 'DeviceMap', 'Category', 'Access', 'Default', 'SafeLevel',
                    'EncType', 'MaxLog', 'MaxPhys', 'MaxPhysLimit', 'MaxBitVal', 'MinLog', 'MinPhys', 'MinPhysLimit',
                    'MinBitVal']
    WITH_APOSTROPHE = ['Name', 'SignalType', 'Device', 'Label', 'DeviceMap', 'Category', 'Access', 'SafeLevel',
                       'EncType']
    WITHOUT_APOSTROPHE = set(COLUMNS_NAME).difference(set(WITH_APOSTROPHE))
    DEFAULT_VALUE_FOR_COLUMNS = {'Name': 'NAN', 'SignalType': 'NAN', 'Device': 'NAN',
                                 'Label': 'NAN', 'DeviceMap': 'NAN', 'Category': 'NAN',
                                 'Access': 'NAN', 'Default': np.NaN, 'SafeLevel': 'NAN',
                                 'EncType': 'NAN', 'MaxLog': np.NaN, 'MaxPhys': np.NaN,
                                 'MaxPhysLimit': np.NaN, 'MaxBitVal': np.NaN, 'MinLog': np.NaN,
                                 'MinPhys': np.NaN, 'MinPhysLimit': np.NaN, 'MinBitVal': np.NaN}
    AVAILABLE_NULL_NAME = {'Name': False, 'SignalType': False, 'Device': False,
                           'Label': True, 'DeviceMap': False, 'Category': True,
                           'Access': True, 'Default': True, 'SafeLevel': True,
                           'EncType': True, 'MaxLog': True, 'MaxPhys': True,
                           'MaxPhysLimit': True, 'MaxBitVal': True, 'MinLog': True,
                           'MinPhys': True, 'MinPhysLimit': True, 'MinBitVal': True}
    AVAILABLE_SIGNALS_PARAM = {'SignalType': ['AI', 'AO', 'DI', 'DO', 'GI', 'GO'],
                               'SafeLevel': ['SAFETYSAFELEVEL'],  # usuniete NANy
                               'Access': ['READONLY'],
                               'EncType': ['UNSIGNED', 'SIGNED']}

    INPUT_LABELS = ['DI', 'AI', 'GI']
    OUTPUT_LABELS = ['DO', 'AO', 'GO']

    MAX_LENGTH_OF_NAME = 32
    REGEX_FOR_MAPPING = r'(\d{1,4})(-\d{1,4})?'
    REGEX_FOR_LABEL = r'[\w _]+'
    REGEX_FOR_NAME = r'[a-zA-Z][_a-zA-Z0-9]+'
    REGEX_FOR_SORTING_BY_DEVICE_MAP = '(\d+).?'
    REGEX_FOR_FIND_START_OF_SIGNAL_DESCRIPTION = r'EIO_SIGNAL:(.*)'
    REGEX_FOR_USER_NAMES = {'Name': REGEX_FOR_NAME, 'Device': REGEX_FOR_NAME, 'Label': REGEX_FOR_LABEL,
                            'DeviceMap': REGEX_FOR_MAPPING, 'Category': REGEX_FOR_NAME}

import os
import sys
import numpy
from ToEIOConverter import SignalsConverter

path_to_excel = r'H:\PythonProjects\ABB_EIO_translation\files\EIO_test1.xlsx'

converter = SignalsConverter.from_excel(path_to_excel)
converter.set_type_for_columns(['Label', 'Category', 'Access', 'SafeLevel', 'EncType'], 'str')
converter.strip_columns(['SignalType', 'Access', 'SafeLevel', 'EncType'])
converter.set_str_to_uppercase(['Label', 'Category', 'Access', 'SafeLevel', 'EncType'])
converter.data.loc[1, 'Name'] = 'dsd$'
converter.check_all_cells()
print(converter.data)


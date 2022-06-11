import os
import sys
import numpy
from ToEIOConverter import SignalsConverter

path_to_excel = r'H:\PythonProjects\ABB_EIO_translation\files\EIO_test1.xlsx'

converter = SignalsConverter.from_excel(path_to_excel)

print(converter.data)


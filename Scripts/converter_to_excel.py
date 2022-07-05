import os
import sys
import numpy
from EIOConverter import SignalsConverterToExcel

if __name__ == '__main__':
    path_to_cfg = r'H:\PythonProjects\ABB_EIO_translation\files\EIO_test_2.cfg'

    converter = SignalsConverterToExcel.from_cfg(path_to_cfg)
    converter.sort_data_frame()
    converter.write_to_excel(r'H:\PythonProjects\ABB_EIO_translation\files\result_excel_1.xlsx')



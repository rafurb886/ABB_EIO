from EIOConverter import SignalsConverterToCfg

if __name__ == '__main__':
    path_to_excel = r'H:\PythonProjects\ABB_EIO_translation\files\EIO_test1.xlsx'

    converter = SignalsConverterToCfg.from_excel(path_to_excel)
    converter.set_type_for_columns(['Label', 'Category', 'Access', 'SafeLevel', 'EncType'], 'str')
    converter.strip_columns(['SignalType', 'Access', 'SafeLevel', 'EncType'])
    converter.set_str_to_uppercase(['Category', 'Access', 'SafeLevel', 'EncType'])
    converter.set_nan_str_to_uppercase(['Label'])

    #converter.data.loc[1, 'Name'] = 'dsd$'
    converter.check_all_cells()
    converter.write_signals_to_cfg(r'H:\PythonProjects\ABB_EIO_translation\files\result_cfg_1.cfg')
    print(converter.data)


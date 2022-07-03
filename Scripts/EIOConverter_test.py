import pytest
import mock
import builtins
from EIOConverter import SignalsConverterToCfg, ValidateSignalsCellsInLine


paths_to_excel = [  r'H:\PythonProjects\ABB_EIO_translation\files\EIO_test1.xlsx',
                    r'H:\PythonProjects\ABB_EIO_translation\files\EIO_test2_1.xlsx',
                    r'H:\PythonProjects\ABB_EIO_translation\files\EIO_test2_2.xlsx']
# 0 - dobry
# 1 - złe wartości
# 2 - brak kolumn

df_imported_from_excel = [SignalsConverterToCfg.from_excel(path) for path in paths_to_excel]


@pytest.mark.parametrize('df', df_imported_from_excel)
def test_import_from_excel(df):
    assert df is not None


@pytest.mark.parametrize('df, rows, columns',  [(df_imported_from_excel[0], 47, 18),
                                                (df_imported_from_excel[1], 47, 18),
                                                (df_imported_from_excel[2], 47, 18)])
def test_import_from_excel_count_columns_and_rows(df, columns, rows):
    assert df.data.shape[0] == rows
    assert df.data.shape[1] == columns


@pytest.mark.parametrize('df', df_imported_from_excel)
def test_columns_name(df):
    assert list(df.data.columns.values) == list(SignalsConverterToCfg.columns_name)


def test_set_upper_case():
    df_imported_from_excel[0].set_type_for_columns(['Label', 'Category', 'Access', 'SafeLevel', 'EncType'], 'str')
    df_imported_from_excel[0].set_str_to_uppercase(['Category', 'Access', 'SafeLevel', 'EncType'])
    assert df_imported_from_excel[0].data['Access'].str.isupper().all()


@pytest.mark.parametrize('string_to_check, result, available_null', [('TestowaNazwa', True, False),
                                                                     ('Testowa_Nazwa', True, False),
                                                                     ('Testowa*Nazwa', False, False),
                                                                     ('', False, True)])
def test_check_correct_characters(string_to_check, result, available_null):
    test_result = ValidateSignalsCellsInLine.check_correct_character(string_to_check, available_null=available_null)
    assert (test_result is not None) == result


@pytest.mark.parametrize('column, wrong_value, user_input', [('Label',      'asd#',     'SI pp_tp_main'),
                                                             ('DeviceMap',  '12314',    '0'),
                                                             ('Name',       'asd#',     'DI_PP_To_Main')])
def test_check_correct_characters_in_columns(column, wrong_value, user_input):
    correct_line = ValidateSignalsCellsInLine(df_imported_from_excel[0].data.loc[0])
    line_to_check = ValidateSignalsCellsInLine(correct_line.line.copy())
    line_to_check.line[column] = wrong_value
    assert line_to_check.line.values.tolist() != correct_line.line.values.tolist()
    with mock.patch.object(builtins, 'input', lambda _: user_input):
        line_to_check.check_correct_character_in_columns([column])
    assert line_to_check.line.values.tolist() == correct_line.line.values.tolist()


@pytest.mark.parametrize('column, wrong_value, user_input', [('Access',     'asd#',     'READONLY'),
                                                             ('SafeLevel',  '12314',    'SAFETYSAFELEVEL'),
                                                             ('EncType',    'asd#',     'UNSIGNED')])
def test_check_correct_parameters_in_columns(column, wrong_value, user_input):
    correct_line = ValidateSignalsCellsInLine(df_imported_from_excel[0].data.loc[0].copy())
    correct_line.line.loc[column] = user_input
    line_to_check = ValidateSignalsCellsInLine(correct_line.line.copy())
    line_to_check.line[column] = wrong_value
    assert line_to_check.line.values.tolist() != correct_line.line.values.tolist()
    with mock.patch.object(builtins, 'input', lambda _: user_input):
        line_to_check.check_correct_parameters_in_columns([column])
    assert line_to_check.line.values.tolist() == correct_line.line.values.tolist()


@pytest.mark.parametrize('column, wrong_value, user_input', [('MaxPhys',     'asd',     1)])
def test_check_is_digit(column, wrong_value, user_input):
    correct_line = ValidateSignalsCellsInLine(df_imported_from_excel[0].data.loc[0].copy())
    correct_line.line.loc[column] = user_input
    line_to_check = ValidateSignalsCellsInLine(correct_line.line.copy())
    line_to_check.line[column] = wrong_value
    assert line_to_check.line.values.tolist() != correct_line.line.values.tolist()
    with mock.patch.object(builtins, 'input', lambda _: user_input):
        line_to_check.check_is_digit([column])
    assert line_to_check.line.values.tolist() == correct_line.line.values.tolist()


@pytest.mark.parametrize('column, wrong_value, user_input, df, result', [('Default', 5,     1,  df_imported_from_excel[0].data.loc[0], True),
                                                                         ('Default', 'asd', 1,  df_imported_from_excel[0].data.loc[0], True),
                                                                         ('Default', 1,  10, df_imported_from_excel[0].data.loc[0], False),
                                                                         ('Default', 'asd', 10, df_imported_from_excel[0].data.loc[45], True),
                                                                         ('Default', 10.3,  10, df_imported_from_excel[0].data.loc[45], True),
                                                                         ('Default', 3,  10, df_imported_from_excel[0].data.loc[45], False)])
def test_check_default_value(column, wrong_value, user_input, df, result):
    correct_line = ValidateSignalsCellsInLine(df.copy())
    correct_line.line.loc[column] = user_input
    line_to_check = ValidateSignalsCellsInLine(correct_line.line.copy())
    line_to_check.line[column] = wrong_value
    assert line_to_check.line.values.tolist() != correct_line.line.values.tolist()
    with mock.patch.object(builtins, 'input', lambda _: user_input):
        line_to_check.check_default_column()
    assert (line_to_check.line.values.tolist() == correct_line.line.values.tolist()) == result


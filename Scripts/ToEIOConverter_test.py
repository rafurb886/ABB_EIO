import pytest
from ToEIOConverter import SignalsConverter


paths_to_excel = [  r'H:\PythonProjects\ABB_EIO_translation\files\EIO_test1.xlsx',
                    r'H:\PythonProjects\ABB_EIO_translation\files\EIO_test2_1.xlsx',
                    r'H:\PythonProjects\ABB_EIO_translation\files\EIO_test2_2.xlsx']
# 0 - dobry
# 1 - złe wartości
# 2 - brak kolumn

df_imported_from_excel = [SignalsConverter.from_excel(path) for path in paths_to_excel]


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
    assert list(df.data.columns.values) == list(SignalsConverter.columns_name)


def test_set_upper_case():
    df_imported_from_excel[0].set_type_for_columns(['Label', 'Category', 'Access', 'SafeLevel', 'EncType'], 'str')
    df_imported_from_excel[0].set_str_to_uppercase(['Category', 'Access', 'SafeLevel', 'EncType'])
    assert df_imported_from_excel[0].data['Access'].str.isupper().all()





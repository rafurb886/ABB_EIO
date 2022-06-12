import pytest
from ToEIOConverter import SignalsConverter


@pytest.fixture
def path_to_excel():
    return r'H:\PythonProjects\ABB_EIO_translation\files\EIO_test1.xlsx'


@pytest.fixture
def df_imported_from_excel(path_to_excel):
    return SignalsConverter.from_excel(path_to_excel)


def test_import_from_excel(df_imported_from_excel):
    assert df_imported_from_excel is not None


def test_import_from_excel_count_columns_and_rows(df_imported_from_excel):
    assert df_imported_from_excel.data.shape[0] == 47
    assert df_imported_from_excel.data.shape[1] == 18


def test_columns_name(df_imported_from_excel):
    assert list(df_imported_from_excel.data.columns.values) == list(SignalsConverter.columns_name)





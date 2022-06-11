import pandas
import regex


def check_uniqe_val_in_column(df, column_name):
    return df[column_name].is_unique


def drop_column_if_exist(df, column_name):
    if not isinstance(column_name, list):
        return df.drop(column_name, axis=1, inplace=True)
    for column in column_name:
        try:
            df.drop(column_name, axis=1, inplace=True)
        except Exception as e:
            print(e)
    return df




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


def add_column_if_no_exist(df, columns_name, default_value):
    for column in columns_name:
        if column not in df.columns:
            df[column] = default_value[column]
    return df


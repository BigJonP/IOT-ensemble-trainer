from typing import Optional

import pandas as pd


def fetch_headers(path: str) -> tuple:
    headers = []
    for col in pd.read_csv(path).columns:
        headers.append(col)
    return tuple(headers)


def data_split(df: pd.DataFrame, y_header: str) -> tuple:
    y = df[y_header]
    x = df.drop(y_header, axis=1)
    return x, y


def load_data(data_file_path: str) -> pd.DataFrame:
    return pd.read_csv(data_file_path)

import os
import pandas as pd


def data_split(data_dir: str, y_header: str) -> tuple:
    df = pd.DataFrame()

    for file in os.listdir(data_dir):
        f = os.path.join(data_dir, file)
        curr_df = pd.read_csv(f)
        df = pd.concat([df, curr_df])

    x = df.loc[:, df.columns != y_header]
    y = df[y_header]

    return (x, y)

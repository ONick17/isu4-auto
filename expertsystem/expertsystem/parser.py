import pandas as pd


def parse(path: str):
    data = pd.read_csv(path, delimiter=' ')
    print(data)

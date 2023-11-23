import pandas as pd
import matplotlib.pyplot as plt


def parse(path: str):
    data = pd.read_csv(path,
                       delimiter='\t',
                       dtype=float,
                       usecols=(1, 2, 3, 4, 5))
    # plt.ion()
    # show(data)
    return data


def show(data: pd.DataFrame):
    print(list(data.keys()))
    for building in list(data.keys()):
        # plt.legend(list(data.keys()))
        plt.plot(data[building], label=building)
        plt.legend()
        plt.draw()
        
    plt.waitforbuttonpress(0)

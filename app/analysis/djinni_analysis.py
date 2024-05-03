from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd


def read_data(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename)


def get_most_common_technologies(path_to_csv: str) -> None:
    df = read_data(path_to_csv)
    df_common = pd.DataFrame(Counter(
        " ".join(df["description"]).split()
    ).most_common(20))
    df_common.set_index(0, inplace=True)
    df_common.plot(kind="bar", title="The Popularity of Technologies",
                   xlabel="Technologies", ylabel="Count", rot=60)
    plt.show()


def get_correlation_matrix(path_to_csv: str) -> None:
    df = read_data(path_to_csv)
    print(df[["experience", "views", "applications"]].corr())

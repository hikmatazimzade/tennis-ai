import pandas as pd

from config import ROOT_DIR


def attach_datasets(start_year: int=1968, end_year: int=2024) -> pd.DataFrame:
    attached_df = []
    for year in range(start_year, end_year + 1):
        curr_df = pd.read_csv(f"{ROOT_DIR}/data/atp_matches_{year}.csv")
        attached_df.append(curr_df)

    return pd.concat(attached_df, ignore_index=True)


if __name__ == '__main__':
    attached_df = attach_datasets()
    print(attached_df.isnull().sum())
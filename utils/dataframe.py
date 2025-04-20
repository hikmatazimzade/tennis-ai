from typing import List
from random import randint

import pandas as pd
from pandas import DataFrame

from config import ROOT_DIR
from utils.logger import get_logger

logger = get_logger("utils.logger")

def get_attached_dataset(start_year: int=1968,
                         end_year: int=2024) -> pd.DataFrame:
    attached_df = []
    for year in range(start_year, end_year + 1):
        curr_df = pd.read_csv(f"{ROOT_DIR}/data/atp_matches_{year}.csv")
        attached_df.append(curr_df)

    return pd.concat(attached_df, ignore_index=True)


def save_attached_dataset(start_year: int=1968,
                         end_year: int=2024) -> None:
    save_path = f"{ROOT_DIR}/data/atp_matches_train.csv"
    try:
        attached_df = get_attached_dataset(start_year, end_year)
        attached_df.to_csv(save_path)
        logger.info(f"Train dataset successfully saved to {save_path}")

    except Exception as save_error:
        logger.error(
            f"Error occurred while saving attached dataset -> {save_error}"
        )


def get_shuffled_dataframe(df: DataFrame) -> DataFrame:
    winner_cols = get_winner_cols(df)
    loser_cols = get_loser_cols(df)
    remaining_cols = get_remaining_cols(df)

    return df


def get_winner_cols(df: DataFrame) -> List[str]:
    return [d for d in df if d.startswith("winner_")]


def get_loser_cols(df: DataFrame) -> List[str]:
    return [d for d in df if d.startswith("loser_")]


def get_remaining_cols(df: DataFrame) -> List[str]:
    return [d for d in df if not d.startswith("winner_") and
            not d.startswith("loser_")]


if __name__ == '__main__':
    save_attached_dataset()

    from data_processing.data_preprocessing import CleanDf
    class DummyCleaner(CleanDf):
        def handle_nan_seed_values(self):
            pass

    cleaner = DummyCleaner()
    cleaner.clean()

    df = cleaner.df
    shuffled_df = get_shuffled_dataframe(df)
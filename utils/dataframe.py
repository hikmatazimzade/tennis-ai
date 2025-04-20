from typing import List
from random import randint

import pandas as pd
from pandas import DataFrame

from utils.logger import get_logger

logger = get_logger("utils.dataframe")


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
    from data_processing.data_preprocessing import CleanDf
    class DummyCleaner(CleanDf):
        def handle_nan_seed_values(self):
            pass

    cleaner = DummyCleaner()
    cleaner.clean()

    df = cleaner.df
    shuffled_df = get_shuffled_dataframe(df)
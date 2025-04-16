from abc import ABC, abstractmethod
from typing import Tuple

import pandas as pd

from config import ROOT_DIR
from utils.logger import get_logger

TRAIN_CSV = f"{ROOT_DIR}/data/atp_matches_train.csv"
logger = get_logger("data_processing.clean")


class CleanDf(ABC):
    def __init__(self):
        self.df = pd.read_csv(TRAIN_CSV)

    def clean(self):
        self.drop_columns()
        self.encode_tourney_date()
        self.apply_one_hot_encoding()

    def drop_columns(self, column_names: Tuple[str]=(
        "tourney_name", "match_num", "winner_name", "loser_name",
        "score", "best_of", "round", "minutes"
    )) -> None:
        for column in column_names:
            try:
                self.df.drop(column, axis=1, inplace=True)
                logger.info(f"{column} column successfully dropped")
            except Exception as column_drop_error:
                logger.error("An error occurred when "
                             f"dropping {column} -> {column_drop_error}")

    def encode_tourney_date(self):
        self.df["tourney_date"] = pd.to_datetime(self.df
            ["tourney_date"].astype(str), format='%Y%m%d')

        self.df['tourney_year'] = self.df['tourney_date'].dt.year
        self.df['tourney_month'] = self.df['tourney_date'].dt.month
        self.df['tourney_day'] = self.df['tourney_date'].dt.day

        self.df.drop(columns=["tourney_date"], inplace=True)

    def apply_one_hot_encoding(self, column_names: Tuple[str]=(
        "surface", "tourney_level", "winner_entry", "winner_hand"
    )) -> None:
        column_names = list(column_names)
        self.df = pd.get_dummies(self.df, columns=column_names)
        logger.info(f"Applied one-hot encoding to {column_names}")


if __name__ == '__main__':
    clean_df = CleanDf()
    clean_df.clean()

    print(clean_df.df.info())
    print(clean_df.df["tourney_year"].unique())
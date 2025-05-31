from abc import ABC, abstractmethod
from typing import Tuple

import pandas as pd

from config import ROOT_DIR
from utils.logger import get_logger

TRAIN_CSV = f"{ROOT_DIR}/data/atp_matches_train.csv"
logger = get_logger("data_processing.data_preprocessing")


class CleanDf(ABC):
    def __init__(self, train_csv: str=TRAIN_CSV):
        self.df = pd.read_csv(train_csv)
        self.cleaning_steps = [
            self.rename_player_columns,
            self.replace_hands,
            self.encode_tourney_date,
            self.apply_one_hot_encoding,
            self.drop_columns,
            self.handle_ambidextrous_hand,

            self.handle_nan_seed_values,
            self.handle_seed_values,
            self.handle_ranks,
            self.drop_all_remaining_nans,
            self.handle_winner_loser_ioc_values,
        ]

    def clean(self) -> pd.DataFrame:
        for step in self.cleaning_steps:
            step()

        return self.df

    def rename_player_columns(self) -> None:
        self.df.columns = [
            col.replace("w_", "winner_") if col.startswith("w_")
            else col.replace("l_", "loser_") if col.startswith("l_")
            else col
            for col in self.df.columns
        ]

    def drop_columns(self, column_names: Tuple[str]=(
        "tourney_name", "tourney_id", "match_num", "winner_name",
        "loser_name", "score", "best_of", "round", "minutes",
        "loser_entry_S", "Unnamed: 0"
    )):
            dropped_columns = []
            for column in column_names:
                try:
                    self.df.drop(column, axis=1, inplace=True)
                    dropped_columns.append(column)
                except Exception as column_drop_error:
                    logger.error("An error occurred when "
                                 f"dropping {column} -> {column_drop_error}")

            logger.info(f"Columns successfully dropped -> {dropped_columns}")

    def encode_tourney_date(self) -> None:
        self.df["tourney_date"] = pd.to_datetime(self.df
            ["tourney_date"].astype(str), format='%Y%m%d')

        self.df['tourney_year'] = self.df['tourney_date'].dt.year
        self.df['tourney_month'] = self.df['tourney_date'].dt.month
        self.df['tourney_day'] = self.df['tourney_date'].dt.day

        self.df.drop(columns=["tourney_date"], inplace=True)

    def apply_one_hot_encoding(self, column_names: Tuple[str]=(
        "surface", "tourney_level", "winner_entry", "loser_entry",
                "winner_hand", "loser_hand"
    )) -> None:
        column_names = list(column_names)
        self.df = pd.get_dummies(self.df, columns=column_names)
        logger.info(f"Applied one-hot encoding to {column_names}")

    def replace_hands(self) -> None:
        self.df.fillna({"winner_hand": "R"}, inplace=True)
        self.df.fillna({"loser_hand": "R"}, inplace=True)
        self.df.replace({"winner_hand": {"U": "R"},
                         "loser_hand": {"U": "R"}}, inplace=True)

    def handle_ambidextrous_hand(self) -> None:
        for prefix in ["winner_hand", "loser_hand"]:
            a_col = f"{prefix}_A"
            r_col = f"{prefix}_R"
            l_col = f"{prefix}_L"

            if a_col in self.df.columns:
                condition = self.df[a_col] == True
                self.df.loc[condition, r_col] = True
                self.df.loc[condition, l_col] = True

        self.df.drop(columns=["winner_hand_A", "loser_hand_A"], inplace=True)

    def handle_seed_values(self) -> None:
        self.df["winner_seed"] = 1 / self.df["winner_seed"]
        self.df["loser_seed"] = 1 / self.df["loser_seed"]

    @abstractmethod
    def handle_nan_seed_values(self) -> None:
        pass

    @abstractmethod
    def handle_winner_loser_ioc_values(self) -> None:
        pass

    def apply_clip(self, cap: int=3000, column_names: Tuple[str]=(
        "winner_rank", "loser_rank"
    )) -> None:
        for column in column_names:
            self.df[column] = self.df[column].clip(upper=cap)
            self.df[column] = self.df[column].clip(upper=cap)

    def handle_ranks(self) -> None:
        self.apply_clip()
        self.df["winner_rank"] = 1 / self.df["winner_rank"]
        self.df["loser_rank"] = 1 / self.df["loser_rank"]

    def drop_all_remaining_nans(self) -> None:
        before = len(self.df)
        self.df.dropna(inplace=True)
        after = len(self.df)
        logger.info(f"{before - after} rows dropped")


if __name__ == '__main__':
    from data_processing.random_forest import CleanRandomForestDf

    clean_df = CleanRandomForestDf().clean()
    print(clean_df.info())
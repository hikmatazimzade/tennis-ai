from abc import ABC, abstractmethod
from typing import Tuple

import pandas as pd

from config import ROOT_DIR
from utils.logger import get_logger

TRAIN_CSV = f"{ROOT_DIR}/data/atp_matches_train.csv"
logger = get_logger("data_processing.clean")


class CleanDf(ABC):
    def __init__(self, train_csv: str=TRAIN_CSV):
        self.df = pd.read_csv(train_csv)

    def clean(self) -> pd.DataFrame:
        self.replace_hands()
        self.drop_columns()
        self.encode_tourney_date()
        self.apply_one_hot_encoding()
        self.handle_ambidextrous_hand()
        self.handle_nan_seed_values()
        self.handle_seed_values()
        self.handle_ranks()
        self.drop_all_remaining_nans() # TODO: Modify it for tree-based models
        return self.df

    def drop_columns(self, column_names: Tuple[str]=(
        "tourney_name", "tourney_id", "match_num", "winner_name", "loser_name",
        "score", "best_of", "round", "minutes", "w_ace", "l_ace", "w_df",
        "l_df", "w_svpt", "l_svpt", "w_1stIn", "l_1stIn", "w_1stWon",
        "l_1stWon", "w_2ndWon", "l_2ndWon", "w_SvGms", "l_SvGms", "w_bpSaved",
        "l_bpSaved", "w_bpFaced", "l_bpFaced"
    )) -> None:
        for column in column_names:
            try:
                self.df.drop(column, axis=1, inplace=True)
                logger.info(f"{column} column successfully dropped")
            except Exception as column_drop_error:
                logger.error("An error occurred when "
                             f"dropping {column} -> {column_drop_error}")

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

    def handle_ambidextrous_hand(self):
        for prefix in ["winner_hand", "loser_hand"]:
            a_col = f"{prefix}_A"
            r_col = f"{prefix}_R"
            l_col = f"{prefix}_L"

            if a_col in self.df.columns:
                condition = self.df[a_col] == True
                self.df.loc[condition, r_col] = True
                self.df.loc[condition, l_col] = True

        self.df.drop(columns=["winner_hand_A", "loser_hand_A"], inplace=True)

    def handle_seed_values(self):
        self.df["winner_seed"] = 1 / self.df["winner_seed"]
        self.df["loser_seed"] = 1 / self.df["loser_seed"]

    @abstractmethod
    def handle_nan_seed_values(self):
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
    class DummyCleaner(CleanDf):
        def handle_nan_seed_values(self):
            pass

    clean_df = DummyCleaner()
    clean_df.clean()

    print(clean_df.df.info())
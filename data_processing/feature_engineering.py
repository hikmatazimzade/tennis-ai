from abc import ABC, abstractmethod
from typing import Tuple, List
from collections import defaultdict

import pandas as pd

from utils.logger import get_logger

logger = get_logger("data_processing.feature_engineering")


def get_elos(df: pd.DataFrame, K:int) -> Tuple[list, list]:
    elo_rating = defaultdict(lambda: 1500)
    player_1_elos = []
    player_2_elos = []

    for _, row in df.iterrows():
        player_1_id, player_2_id = row["player_1_id"], row["player_2_id"]
        player_1_won = row["player_1_won"]

        append_elos(player_1_elos, player_2_elos, player_1_id,
                    player_2_id, elo_rating)
        update_elo(elo_rating, player_1_won, K, player_1_id, player_2_id)

    return player_1_elos, player_2_elos


def update_elo(elo_rating: dict, player_1_won: bool, K: int, player_1_id: int,
               player_2_id: int) -> None:
    actual_score_1 = 1 if player_1_won else 0
    actual_score_2 = 1 - actual_score_1

    expected_score_1 = get_expected_score(elo_rating[player_1_id],
                                          elo_rating[player_2_id])
    expected_score_2 = 1 - expected_score_1

    elo_rating[player_1_id] += K * (actual_score_1 - expected_score_1)
    elo_rating[player_2_id] += K * (actual_score_2 - expected_score_2)


def get_expected_score(player_1_elo: float, player_2_elo: float) -> float:
    return 1 / (1 + 10 ** ((player_2_elo - player_1_elo) / 400))


def append_elos(player_1_elos: list, player_2_elos: list, player_1_id: int,
                player_2_id: int, elo_rating) -> None:
    player_1_elos.append(elo_rating[player_1_id])
    player_2_elos.append(elo_rating[player_2_id])


def update_match_dict(match_dt: defaultdict, player_1_won: bool,
                      player_1_id: int, player_2_id: int) -> None:
    if player_1_won:
        match_dt[player_1_id][0] += 1
        for i, num in enumerate([5, 10, 20, 50], start=2):
            match_dt[player_1_id][i] = min(match_dt[player_1_id][i] + 1, num)
            match_dt[player_2_id][i] = max(match_dt[player_2_id][i] - 1, 0)

    else:
        match_dt[player_2_id][0] += 1
        for i, num in enumerate([5, 10, 20, 50], start=2):
            match_dt[player_2_id][i] = min(match_dt[player_2_id][i] + 1, num)
            match_dt[player_2_id][i] = max(match_dt[player_2_id][i] - 1, 0)

    match_dt[player_1_id][1] += 1
    match_dt[player_2_id][1] += 1


class FeatureEngineeringDf(ABC):
    def __init__(self, df: pd.DataFrame):
        self.df = df.sort_values(["tourney_year", "tourney_month",
                                       "tourney_day"])

    def apply_feature_engineering(self) -> pd.DataFrame:
        logger.info("Applying feature engineering")

        self.add_rank_diff()
        self.add_rank_points_diff()
        self.add_height_diff()

        self.create_total_match()
        self.create_won_match()
        self.create_last_won_matches()

        self.create_head_to_head()
        self.fill_head_to_head_won()
        self.add_head_to_head_diff()

        self.fill_total_won_match_data()
        self.add_total_match_diff()
        self.add_won_match_diff()
        self.add_last_won_match_diff()

        self.add_age_diff()
        self.add_elo()
        self.add_elo_diff()
        return self.df

    def add_rank_diff(self) -> None:
        self.df["rank_diff"] = (self.df["player_1_rank"]
                            - self.df["player_2_rank"])

    def add_rank_points_diff(self) -> None:
        self.df["rank_points_diff"] = (self.df["player_1_rank_points"]
                                       - self.df["player_2_rank_points"])

    def add_age_diff(self) -> None:
        self.df["age_diff"] = (self.df["player_1_age"]
                               - self.df["player_2_age"])

    def add_height_diff(self) -> None:
        self.df["height_diff"] = (self.df["player_1_ht"]
                                  - self.df["player_2_ht"])

    def create_head_to_head(self) -> None:
        self.df["player_1_h2h_won"] = 0
        self.df["player_2_h2h_won"] = 0
        self.df["h2h_diff"] = 0

    def create_total_match(self) -> None:
        self.df["player_1_total_match"] = 0
        self.df["player_2_total_match"] = 0

    def create_won_match(self) -> None:
        self.df["player_1_won_match"] = 0
        self.df["player_2_won_match"] = 0

    def create_last_won_matches(self) -> None:
        for num in (5, 10, 20, 50):
            self.df[f"player_1_last_{num}_won"] = 0
            self.df[f"player_2_last_{num}_won"] = 0

    def add_total_match_diff(self) -> None:
        self.df["total_match_diff"] = (self.df["player_1_total_match"]
                                - self.df["player_2_total_match"])

    def add_won_match_diff(self) -> None:
        self.df["won_match_diff"] = (self.df["player_1_won_match"]
                                - self.df["player_2_won_match"])

    def add_last_won_match_diff(self) -> None:
        for idx, num in enumerate([5, 10, 20, 50], start=2):
            self.df[f"last_{num}_match_diff"] = (
                                self.df[f"player_1_last_{num}_won"]
                                - self.df[f"player_2_last_{num}_won"])

    def add_head_to_head_diff(self) -> None:
        self.df["h2h_diff"] = (self.df["player_1_h2h_won"]
                       - self.df["player_2_h2h_won"])

    def fill_head_to_head_won(self) -> defaultdict:
        h2h_dict = defaultdict(lambda: [0, 0])
        for idx, row in self.df.iterrows():
            player_1_id, player_2_id = row["player_1_id"], row["player_2_id"]
            player_1_won = row["player_1_won"]

            if (player_2_id, player_1_id) in h2h_dict:
                key = (player_2_id, player_1_id)
                first, second = 1, 0

            else:
                key = (player_1_id, player_2_id)
                first, second = 0, 1

            self.df.at[idx, "player_1_h2h_won"] = h2h_dict[key][first]
            self.df.at[idx, "player_2_h2h_won"] = h2h_dict[key][second]

            if player_1_won: h2h_dict[key][first] += 1
            else: h2h_dict[key][second] += 1

        return h2h_dict

    def fill_total_won_match_data(self) -> defaultdict:
        match_dt = defaultdict(lambda: [0, 0, 0, 0, 0, 0])
        # index 0 won, 1 total # then last_n_matches results

        for idx, row in self.df.iterrows():
            player_1_id, player_2_id = row["player_1_id"], row["player_2_id"]
            player_1_won = row["player_1_won"]

            self.df.at[idx, "player_1_won_match"] = match_dt[player_1_id][0]
            self.df.at[idx, "player_2_won_match"] = match_dt[player_2_id][0]

            self.df.at[idx, "player_1_total_match"] = match_dt[player_1_id][1]
            self.df.at[idx, "player_2_total_match"] = match_dt[player_2_id][1]

            for i, num in enumerate([5, 10, 20, 50], start=2):
                self.df.at[idx, f"player_1_last_{num}_won"] = (
                                                    match_dt[player_1_id][i])

                self.df.at[idx, f"player_2_last_{num}_won"] = (
                                                    match_dt[player_2_id][i])

            update_match_dict(match_dt, player_1_won,
                              player_1_id, player_2_id)

        return match_dt

    def add_elo(self, K: int=75) -> None:
        self.df = self.df.sort_values(["tourney_year", "tourney_month",
                                       "tourney_day"])
        player_1_elos, player_2_elos = get_elos(self.df, K)

        self.df["player_1_elo"] = player_1_elos
        self.df["player_2_elo"] = player_2_elos

    def add_elo_diff(self) -> None:
        self.df["elo_diff"] = (self.df["player_1_elo"]
                - self.df["player_2_elo"])


if __name__ == '__main__':
    from training.random_forest import CleanRandomForestDf
    from utils.dataframe import shuffle_winner_loser_data

    cleaner = CleanRandomForestDf()
    cleaner.clean()

    df = cleaner.df
    shuffled_df = shuffle_winner_loser_data(df)

    feature_engineering = FeatureEngineeringDf(shuffled_df)
    feature_engineering.apply_feature_engineering()

    df = feature_engineering.df
    print(df.info())
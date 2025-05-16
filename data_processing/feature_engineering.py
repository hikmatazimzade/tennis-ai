from abc import ABC, abstractmethod
from typing import Tuple, List
from collections import defaultdict

import numpy as np
import pandas as pd

from utils.logger import get_logger

logger = get_logger("data_processing.feature_engineering")


def get_elos(df: pd.DataFrame, K:int) -> Tuple[list, list]:
    elo_rating = defaultdict(lambda: 1500)
    player_1_elos = []
    player_2_elos = []

    for row in df.itertuples(index=False):
        player_1_id, player_2_id = row.player_1_id, row.player_2_id
        player_1_won = row.player_1_won

        append_elos(player_1_elos, player_2_elos, player_1_id,
                    player_2_id, elo_rating)
        update_elo(elo_rating, player_1_won, K, player_1_id, player_2_id)

    return player_1_elos, player_2_elos


def get_surface_index(carpet: bool, clay: bool, grass: bool) -> int:
    if carpet: return 0
    if clay: return 1
    if grass: return 2
    else: return 3


def append_surface_elos(player_1_elos: list, player_2_elos: list, player_1_id: int,
                player_2_id: int, elo_rating, surface_idx: int) -> None:
    player_1_elos.append(elo_rating[player_1_id][surface_idx])
    player_2_elos.append(elo_rating[player_2_id][surface_idx])


def update_surface_elo(elo_rating: dict, player_1_won: bool, K: int,
            player_1_id: int, player_2_id: int, surface_idx: int) -> None:
    actual_score_1 = 1 if player_1_won else 0
    actual_score_2 = 1 - actual_score_1

    expected_score_1 = get_expected_score(elo_rating[player_1_id][surface_idx],
                                          elo_rating[player_2_id][surface_idx])
    expected_score_2 = 1 - expected_score_1

    elo_rating[player_1_id][surface_idx] += K * (actual_score_1 - expected_score_1)
    elo_rating[player_2_id][surface_idx] += K * (actual_score_2 - expected_score_2)


def get_surface_elos(df: pd.DataFrame, K: int) -> Tuple[list, list]:
    elo_rating = defaultdict(lambda: [1500, 1500, 1500, 1500])
    # carpet, clay, grass, hard

    player_1_elos = []
    player_2_elos = []

    for row in df.itertuples(index=False):
        carpet, clay = row.surface_Carpet, row.surface_Clay
        grass, hard = row.surface_Grass, row.surface_Hard
        surface_idx = get_surface_index(carpet, clay, grass)

        player_1_id, player_2_id = row.player_1_id, row.player_2_id
        player_1_won = row.player_1_won

        append_surface_elos(player_1_elos, player_2_elos, player_1_id,
                    player_2_id, elo_rating, surface_idx)
        update_surface_elo(elo_rating, player_1_won, K, player_1_id,
                           player_2_id, surface_idx)

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
                      player_1_id: int, player_2_id: int,
                      last_n_matches: tuple) -> None:
    if player_1_won:
        match_dt[player_1_id][0] += 1
        for i, num in enumerate(last_n_matches, start=2):
            match_dt[player_1_id][i] = min(match_dt[player_1_id][i] + 1, num)
            match_dt[player_2_id][i] = max(match_dt[player_2_id][i] - 1, 0)

    else:
        match_dt[player_2_id][0] += 1
        for i, num in enumerate(last_n_matches, start=2):
            match_dt[player_2_id][i] = min(match_dt[player_2_id][i] + 1, num)
            match_dt[player_1_id][i] = max(match_dt[player_1_id][i] - 1, 0)

    match_dt[player_1_id][1] += 1
    match_dt[player_2_id][1] += 1


def append_player_elo_progress(players_elo_history: defaultdict,
            player_id: int, player_elo: float) -> None:
    players_elo_history[player_id].append(player_elo)


class FeatureEngineeringBase(ABC):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    @abstractmethod
    def apply_feature_engineering(self) -> pd.DataFrame:
        pass


class PlayerStatsEngineering(FeatureEngineeringBase):
    def apply_feature_engineering(self) -> pd.DataFrame:
        self.add_rank_feature_differences()
        self.add_seed_diff()
        return self.df

    def add_rank_feature_differences(self) -> None:
        self.add_rank_diff()
        self.add_rank_points_diff()

    def add_seed_diff(self) -> None:
        self.df["seed_diff"] = (self.df["player_1_seed"]
                            - self.df["player_2_seed"])

    def add_rank_diff(self) -> None:
        self.df["rank_diff"] = (self.df["player_1_rank"]
                            - self.df["player_2_rank"])

    def add_rank_points_diff(self) -> None:
        self.df["rank_points_diff"] = (self.df["player_1_rank_points"]
                                       - self.df["player_2_rank_points"])


class PhysicalEngineering(FeatureEngineeringBase):
    def apply_feature_engineering(self) -> pd.DataFrame:
        self.add_player_physical_features()
        return self.df

    def add_player_physical_features(self) -> None:
        self.add_height_diff()
        self.add_age_diff()

    def add_age_diff(self) -> None:
        self.df["age_diff"] = (self.df["player_1_age"]
                               - self.df["player_2_age"])

    def add_height_diff(self) -> None:
        self.df["height_diff"] = (self.df["player_1_ht"]
                                  - self.df["player_2_ht"])


class CreateMatchFeatures(FeatureEngineeringBase):
    def __init__(self, df: pd.DataFrame, last_n_matches: tuple):
        super().__init__(df)
        self.last_n_matches = last_n_matches

    def apply_feature_engineering(self) -> pd.DataFrame:
        self.create_last_won_matches()
        return self.df

    def create_last_won_matches(self) -> None:
        for num in self.last_n_matches:
            self.df[f"player_1_last_{num}_match_won"] = 0
            self.df[f"player_2_last_{num}_match_won"] = 0


class HeadToHeadEngineering(FeatureEngineeringBase):
    def apply_feature_engineering(self) -> pd.DataFrame:
        self.add_head_to_head_features()
        return self.df

    def add_head_to_head_features(self) -> None:
        self.fill_head_to_head_won()
        self.add_head_to_head_diff()

        self.fill_surface_head_to_head_won()
        self.add_surface_head_to_head_diff()

    def add_surface_head_to_head_diff(self) -> None:
        self.df["surface_h2h_diff"] = (self.df["player_1_surface_h2h_won"]
                                    - self.df["player_2_surface_h2h_won"])

    def fill_surface_head_to_head_won(self) -> defaultdict:
        surface_h2h_dict = defaultdict(lambda: [[0, 0], [0, 0],
                                                [0, 0], [0, 0]])
        player_1_surface_h2h_won, player_2_surface_h2h_won = [], []

        for row in self.df.itertuples():
            player_1_id, player_2_id = row.player_1_id, row.player_2_id
            player_1_won = row.player_1_won

            if (player_2_id, player_1_id) in surface_h2h_dict:
                key = (player_2_id, player_1_id)
                first, second = 1, 0

            else:
                key = (player_1_id, player_2_id)
                first, second = 0, 1

            carpet, clay = row.surface_Carpet, row.surface_Clay
            grass, hard = row.surface_Grass, row.surface_Hard
            surface_idx = get_surface_index(carpet, clay, grass)

            player_1_surface_h2h_won.append(surface_h2h_dict
                                            [key][surface_idx][first])
            player_2_surface_h2h_won.append(surface_h2h_dict
                                            [key][surface_idx][second])

            if player_1_won:
                surface_h2h_dict[key][surface_idx][first] += 1
            else:
                surface_h2h_dict[key][surface_idx][second] += 1

        self.df["player_1_surface_h2h_won"] = player_1_surface_h2h_won
        self.df["player_2_surface_h2h_won"] = player_2_surface_h2h_won

        return surface_h2h_dict

    def fill_head_to_head_won(self) -> defaultdict:
        h2h_dict = defaultdict(lambda: [0, 0])
        player_1_h2h_won, player_2_h2h_won = [], []

        for row in self.df.itertuples():
            player_1_id, player_2_id = row.player_1_id, row.player_2_id
            player_1_won = row.player_1_won

            if (player_2_id, player_1_id) in h2h_dict:
                key = (player_2_id, player_1_id)
                first, second = 1, 0

            else:
                key = (player_1_id, player_2_id)
                first, second = 0, 1

            player_1_h2h_won.append(h2h_dict[key][first])
            player_2_h2h_won.append(h2h_dict[key][second])

            if player_1_won: h2h_dict[key][first] += 1
            else: h2h_dict[key][second] += 1

        self.df["player_1_h2h_won"] = player_1_h2h_won
        self.df["player_2_h2h_won"] = player_2_h2h_won

        return h2h_dict

    def add_head_to_head_diff(self) -> None:
        self.df["h2h_diff"] = (self.df["player_1_h2h_won"]
                       - self.df["player_2_h2h_won"])


class MatchDataEngineering(FeatureEngineeringBase):
    def __init__(self, df: pd.DataFrame, last_n_matches: tuple):
        super().__init__(df)
        self.last_n_matches = last_n_matches

    def apply_feature_engineering(self) -> pd.DataFrame:
        self.fill_total_won_match_data()
        return self.df

    def fill_total_won_match_data(self) -> defaultdict:
        match_dt = defaultdict(lambda: [0, 0]
            + len(self.last_n_matches) * [0])
        # index 0 won, 1 total, then last_n_matches results
        player_1_won_match, player_2_won_match = [], []
        player_1_total_match, player_2_total_match = [], []
        last_won_matches_1, last_won_matches_2 = [], []

        for row in self.df.itertuples():
            player_1_id, player_2_id = row.player_1_id, row.player_2_id
            player_1_won = row.player_1_won

            player_1_won_match.append(match_dt[player_1_id][0])
            player_2_won_match.append(match_dt[player_2_id][0])

            player_1_total_match.append(match_dt[player_1_id][1])
            player_2_total_match.append(match_dt[player_2_id][1])

            self.append_last_won_matches(match_dt, player_1_id, player_2_id,
                                    last_won_matches_1, last_won_matches_2)

            self.update_matches_dict(match_dt, player_1_id,
                                     player_2_id, player_1_won)

        self.df["player_1_won_match"] = player_1_won_match
        self.df["player_2_won_match"] = player_2_won_match

        self.df["player_1_total_match"] = player_1_total_match
        self.df["player_2_total_match"] = player_2_total_match

        self.update_last_won_matches(last_won_matches_1, last_won_matches_2)

        return match_dt

    def update_last_won_matches(self, last_won_matches_1: List[List[int]],
                                last_won_matches_2: List[List[int]]):
        last_won_matches_1 = list(zip(*last_won_matches_1))
        last_won_matches_2 = list(zip(*last_won_matches_2))

        for idx, num in enumerate(self.last_n_matches):
            self.df[f"player_1_last_{num}_match_won"] = (
                last_won_matches_1[idx])

            self.df[f"player_2_last_{num}_match_won"] = (
                last_won_matches_2[idx])

    def append_last_won_matches(self, match_dt: defaultdict, player_1_id: int,
                        player_2_id: int, last_won_matches_1: List[list],
                                last_won_matches_2: List[list]):
        curr_data_1, curr_data_2 = [], []
        for match_idx, num in enumerate(self.last_n_matches, start=2):
            match_data = self.get_last_won_match_data(match_dt, player_1_id,
                                                player_2_id, match_idx)

            curr_data_1.append(match_data[0])
            curr_data_2.append(match_data[1])

        last_won_matches_1.append(curr_data_1)
        last_won_matches_2.append(curr_data_2)

    def get_last_won_match_data(self, match_dt: defaultdict, player_1_id: int,
            player_2_id: int, match_idx: int) -> Tuple[int, int]:
        return (match_dt[player_1_id][match_idx],
                match_dt[player_2_id][match_idx])

    def update_matches_dict(self, match_dt: defaultdict, player_1_id: int,
                            player_2_id: int, player_1_won: bool) -> None:
        update_match_dict(match_dt, player_1_won,
                          player_1_id, player_2_id,
                          self.last_n_matches)


class MatchFeatureDifference(FeatureEngineeringBase):
    def __init__(self, df: pd.DataFrame, last_n_matches: tuple):
        super().__init__(df)
        self.last_n_matches = last_n_matches

    def apply_feature_engineering(self) -> pd.DataFrame:
        self.add_match_feature_differences()
        return self.df

    def add_match_feature_differences(self) -> None:
        self.add_total_match_diff()
        self.add_won_match_diff()
        self.add_last_won_match_diff()

    def add_total_match_diff(self) -> None:
        self.df["total_match_diff"] = (self.df["player_1_total_match"]
                                - self.df["player_2_total_match"])

    def add_won_match_diff(self) -> None:
        self.df["won_match_diff"] = (self.df["player_1_won_match"]
                                - self.df["player_2_won_match"])

    def add_last_won_match_diff(self) -> None:
        for idx, num in enumerate(self.last_n_matches, start=2):
            self.df[f"last_{num}_match_diff"] = (
                                self.df[f"player_1_last_{num}_match_won"]
                                - self.df[f"player_2_last_{num}_match_won"])


class WinRatioEngineering(FeatureEngineeringBase):
    def __init__(self, df: pd.DataFrame, last_n_matches: tuple):
        super().__init__(df)
        self.last_n_matches = last_n_matches

    def apply_feature_engineering(self) -> pd.DataFrame:
        self.add_win_ratio_features()
        return self.df

    def add_win_ratio_features(self) -> None:
        self.add_win_ratio()
        self.add_last_matches_win_ratio()

        self.add_win_ratio_diff()
        self.add_last_matches_win_ratio_diff()

    def add_win_ratio(self) -> None:
        self.df["player_1_win_ratio"] = np.where(
            self.df["player_1_total_match"] == 0,
            0,
            self.df["player_1_won_match"] / self.df["player_1_total_match"]
        )

        self.df["player_2_win_ratio"] = np.where(
            self.df["player_2_total_match"] == 0,
            0,
            self.df["player_2_won_match"] / self.df["player_2_total_match"]
        )

    def add_win_ratio_diff(self) -> None:
        self.df["win_ratio_diff"] = (self.df["player_1_win_ratio"]
                                    - self.df["player_2_win_ratio"])

    def add_last_matches_win_ratio(self) -> None:
        for num in self.last_n_matches:
            self.df[f"player_1_last_{num}_win_ratio"] = (
                    self.df[f"player_1_last_{num}_match_won"] / num
            )

            self.df[f"player_2_last_{num}_win_ratio"] = (
                    self.df[f"player_2_last_{num}_match_won"] / num
            )

    def add_last_matches_win_ratio_diff(self) -> None:
        for num in self.last_n_matches:
            self.df[f"last_{num}_win_ratio_diff"] = (
                self.df[f"player_1_last_{num}_win_ratio"]
                - self.df[f"player_2_last_{num}_win_ratio"]
            )


class EloEngineering(FeatureEngineeringBase):
    def __init__(self, df: pd.DataFrame, last_n_matches: tuple, K: int=24):
        super().__init__(df)
        self.last_n_matches = last_n_matches
        self.K = K

    def apply_feature_engineering(self) -> pd.DataFrame:
        self.add_elo_features()
        return self.df

    def add_elo_features(self) -> None:
        self.add_elo()
        self.add_elo_diff()

        self.add_surface_elo()
        self.add_surface_elo_diff()

        self.add_elo_progress_column()
        self.add_last_matches_elo_progress()

    def add_elo(self) -> None:
        player_1_elos, player_2_elos = get_elos(self.df, self.K)

        self.df["player_1_elo"] = player_1_elos
        self.df["player_2_elo"] = player_2_elos

    def add_elo_diff(self) -> None:
        self.df["elo_diff"] = (self.df["player_1_elo"]
                               - self.df["player_2_elo"])

    def add_surface_elo(self) -> None:
        player_1_elos, player_2_elos = get_surface_elos(self.df, self.K)

        self.df["player_1_surface_elo"] = player_1_elos
        self.df["player_2_surface_elo"] = player_2_elos

    def add_surface_elo_diff(self) -> None:
        self.df["surface_elo_diff"] = (
                self.df["player_1_surface_elo"]
                - self.df["player_2_surface_elo"]
        )

    def add_elo_progress_column(self) -> None:
        for num in self.last_n_matches:
            self.df[f"player_1_last_{num}_elo_progress"] = 0.0
            self.df[f"player_2_last_{num}_elo_progress"] = 0.0

    def add_last_matches_elo_progress(self) -> None:
        players_elo_history = defaultdict(lambda: [])
        for row_idx, row in self.df.iterrows():
            player_1_id, player_2_id = row["player_1_id"], row["player_2_id"]
            player_1_elo = row["player_1_elo"]
            player_2_elo = row["player_2_elo"]

            for last_n in self.last_n_matches:
                player_1_history = players_elo_history[player_1_id]
                player_2_history = players_elo_history[player_2_id]

                self.set_players_elo_progress(players_elo_history, player_1_history,
                    player_2_history, last_n,
                    player_1_id, player_2_id, row_idx)

            append_player_elo_progress(players_elo_history, player_1_id, player_1_elo)
            append_player_elo_progress(players_elo_history, player_2_id, player_2_elo)

    def set_players_elo_progress(self, players_elo_history: defaultdict,
                player_1_history: List[float], player_2_history: List[float],
                last_n: int, player_1_id: int, player_2_id: int, row_idx):
        self.handle_player_elo_progress(players_elo_history,
                                        player_1_history, player_1_id,
                                        last_n, 1, row_idx)

        self.handle_player_elo_progress(players_elo_history,
                                        player_2_history, player_2_id,
                                        last_n, 2, row_idx)

    def handle_player_elo_progress(self, players_elo_history: defaultdict,
                player_history: List[float], player_id: int, last_n: int,
                player_num: int, row_idx) -> None:
        if not player_history:
            new_progress = 0

        elif last_n > len(players_elo_history[player_id]):
            new_progress = player_history[-1]/ player_history[0]

        else:
            new_progress = (player_history[-1]
                            / player_history[len(player_history) - last_n])

        self.df.at[row_idx, (f"player_{player_num}_last_{last_n}"
                             "_elo_progress")] = new_progress


class FeatureEngineeringDf(FeatureEngineeringBase):
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self.df = df.sort_values(["tourney_year", "tourney_month",
                                       "tourney_day"])
        self.last_n_matches = (5, 10, 20, 50)
        self.feature_engineering_steps = [
            PlayerStatsEngineering(self.df).apply_feature_engineering,
            PhysicalEngineering(self.df).apply_feature_engineering,

            (CreateMatchFeatures(self.df, self.last_n_matches)
             .apply_feature_engineering),

            HeadToHeadEngineering(self.df).apply_feature_engineering,

            (MatchDataEngineering(self.df, self.last_n_matches)
            .apply_feature_engineering),

            (MatchFeatureDifference(self.df, self.last_n_matches)
             .apply_feature_engineering),

            (WinRatioEngineering(self.df, self.last_n_matches)
             .apply_feature_engineering),

            (EloEngineering(self.df, self.last_n_matches)
             .apply_feature_engineering)
        ]

    def apply_feature_engineering(self) -> pd.DataFrame:
        logger.info("Applying feature engineering")

        for step in self.feature_engineering_steps:
            step()

        return self.df


if __name__ == '__main__':
    from data_processing.random_forest import CleanRandomForestDf
    from utils.dataframe import shuffle_winner_loser_data

    cleaner = CleanRandomForestDf()
    cleaner.clean()

    df = cleaner.df
    shuffled_df = shuffle_winner_loser_data(df)

    feature_engineering = FeatureEngineeringDf(shuffled_df)
    feature_engineering.apply_feature_engineering()

    df = feature_engineering.df
    print(df.info())
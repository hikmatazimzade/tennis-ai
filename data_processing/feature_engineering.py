from abc import ABC, abstractmethod

import numpy as np

from utils.logger import get_logger
from utils.feature_helpers import *

logger = get_logger("data_processing.feature_engineering")


class FeatureEngineeringBase(ABC):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    @abstractmethod
    def apply_feature_engineering(self) -> pd.DataFrame:
        pass


class InGameDataEngineering(FeatureEngineeringBase):
    def __init__(self, df: pd.DataFrame, last_n_matches: tuple):
        super().__init__(df)
        self.last_n_matches = last_n_matches
        self.in_game_columns = (
            "ace", "df", "svpt", "1stIn",
            "1stWon", "2ndWon", "SvGms",
            "bpSaved", "bpFaced"
        )

    def apply_feature_engineering(self) -> pd.DataFrame:
        self.add_in_game_data()
        self.add_in_game_diff()
        return self.df

    def add_in_game_data(self) -> None:
        col_dict = {}
        for game_column in self.in_game_columns:
            self.process_game_column(game_column, col_dict)

        self.df = bulk_add(self.df, col_dict)

    def process_game_column(self, game_column: str, col_dict: dict) -> None:
        in_game_dict = self.get_final_in_game_dict(game_column)
        player_index_dict = defaultdict(lambda: 5 * [0])

        last_len = len(self.last_n_matches)
        last_n = LastN(last_len)

        player_total_val_dict = defaultdict(int)
        total_val_list_1, total_val_list_2 = [], []

        self.iterate_rows_and_build_features(game_column, in_game_dict,
                    player_index_dict, last_n, player_total_val_dict,
                    total_val_list_1, total_val_list_2)

        self.update_cols(game_column, last_n,
                    total_val_list_1, total_val_list_2, col_dict)
 
    def iterate_rows_and_build_features(self, game_column: str,
            in_game_dict: dict, player_index_dict: defaultdict, last_n: LastN,
            player_total_val_dict: defaultdict, total_val_list_1: List[int],
            total_val_list_2: List[int]) -> None:
        for row in self.df.itertuples():
            ply_1_id, ply_2_id = row.player_1_id, row.player_2_id
            ply_1_index_list = player_index_dict[ply_1_id]
            ply_2_index_list = player_index_dict[ply_2_id]

            handle_in_game_values(row, game_column, total_val_list_1,
                  total_val_list_2, ply_1_id, ply_2_id, player_total_val_dict)

            surface_idx = get_surface_index_by_row(row)
            player_1_list = in_game_dict[ply_1_id]
            player_2_list = in_game_dict[ply_2_id]

            curr_surface_index_1 = ply_1_index_list[surface_idx]
            curr_surface_index_2 = ply_2_index_list[surface_idx]

            self.process_time_windows(
                player_1_list, player_2_list, last_n,
                ply_1_index_list, ply_2_index_list, surface_idx,
                curr_surface_index_1, curr_surface_index_2
            )

            increase_player_indexes(player_index_dict, ply_1_id, ply_2_id,
                            ply_1_index_list, ply_2_index_list, surface_idx)

    def process_time_windows(self, player_1_list: list, player_2_list: list,
            last_n: LastN, ply_1_index_list: list, ply_2_index_list: list,
            surface_idx: int, curr_surface_index_1: int,
                              curr_surface_index_2: int) -> None:
        last_len = len(self.last_n_matches)
        for last in range(last_len):
            append_last_n_lists(player_1_list, player_2_list, last_n, last,
                    ply_1_index_list, ply_2_index_list, surface_idx,
                    curr_surface_index_1, curr_surface_index_2)

    def update_cols(self, game_column: str, last_n: LastN,
            total_val_list_1: List[int], total_val_list_2: List[int],
            col_dict: dict) -> None:
        cols = self.get_in_game_columns_dict(game_column, last_n.last_n_1,
                    last_n.last_n_2, last_n.last_n_surface_1,
                    last_n.last_n_surface_2, total_val_list_1,
                    total_val_list_2)
        col_dict.update(cols)

    def get_in_game_columns_dict(self, game_column: str,
                                 last_n_1: List[List[int]], last_n_2: List[List[int]],
                                 last_n_surface_1: List[List[int]], last_n_surface_2: List[List[int]],
                                 total_val_list_1: List[int], total_val_list_2: List[int]) -> dict:
        cols = {}

        cols.update({
            f"player_1_{game_column}_total": total_val_list_1,
            f"player_2_{game_column}_total": total_val_list_2
        })

        for last_idx, last in enumerate(self.last_n_matches):
            cols.update({
                f"player_1_{game_column}_last_{last}_"
                f"surface": last_n_surface_1[last_idx],
                f"player_2_{game_column}_last_{last}_"
                f"surface": last_n_surface_2[last_idx],
                f"player_1_{game_column}_last_{last}": last_n_1[last_idx],
                f"player_2_{game_column}_last_{last}": last_n_2[last_idx]
            })

        return cols

    def add_in_game_diff(self) -> None:
        col_dict = {}

        for game_column in self.in_game_columns:
            col_dict[f"{game_column}_total_diff"] = (
                self.df[f"player_1_{game_column}_total"]
                - self.df[f"player_2_{game_column}_total"]
            )

            for last in self.last_n_matches:
                col_dict[f"{game_column}_last_{last}_surface_diff"] = (
                        self.df[f"player_1_{game_column}_"
                                f"last_{last}_surface"]
                        - self.df[f"player_2_{game_column}"
                                  f"_last_{last}_surface"]
                )
                col_dict[f"{game_column}_last_{last}_diff"] = (
                        self.df[f"player_1_{game_column}_last_{last}"]
                        - self.df[f"player_2_{game_column}_last_{last}"]
                )

        self.df = bulk_add(self.df, col_dict)

    def get_final_player_dict_over_different_surfaces(self,
                            game_column: str) -> Dict[int, List[List]]:
        player_dict_over_surfaces = get_in_game_dict_over_surfaces()
        self.append_player_dict_over_surfaces(game_column,
                                              player_dict_over_surfaces)
        return player_dict_over_surfaces

    def append_player_dict_over_surfaces(self, game_column: str,
                        player_dict_over_surfaces: defaultdict) -> None:
        for row in self.df.itertuples():
            player_1_val, player_2_val = get_in_game_data_by_row(
                row, game_column)
            player_1_id, player_2_id = row.player_1_id, row.player_2_id

            surface_idx = get_surface_index_by_row(row)
            player_dict_over_surfaces[player_1_id][surface_idx].append(
                player_1_val)

            player_dict_over_surfaces[player_2_id][surface_idx].append(
                player_2_val)

    def get_final_in_game_dict(self, game_column: str) -> dict:
        player_dict_over_surfaces = (
              self.get_final_player_dict_over_different_surfaces(game_column))

        in_game_dict = self.get_in_game_dict(player_dict_over_surfaces)
        return in_game_dict

    def get_in_game_dict(self,
                    player_dict: Dict[int, List[List[int]]]) -> dict:
        in_game_dict = {}

        for player_id in player_dict:
            player_list = (
                    self.get_player_in_game_lists(player_dict[player_id])
            )
            in_game_dict[player_id] = player_list

        return in_game_dict

    def get_player_in_game_lists(self,curr_in_game: List[List[int]]
                                 ) -> List[List[List[int]]]:
        player_in_game_list = [[[] for _ in
                    range(len(self.last_n_matches))] for _ in range(4)]
        # Inside every surface list, there are last n matches data

        for surface_idx, surface_data in enumerate(curr_in_game):
            curr_len = len(surface_data)
            for last_idx, last_n in enumerate(self.last_n_matches):
                for match_idx in range(curr_len):
                    first = max(match_idx - last_n, 0)

                    player_in_game_list[surface_idx][last_idx].append(
                        sum(
                            surface_data[first:match_idx]
                        )
                    )

        return player_in_game_list


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


class HeadToHeadEngineering(FeatureEngineeringBase):
    def apply_feature_engineering(self) -> pd.DataFrame:
        self.add_head_to_head_features()
        return self.df

    def add_head_to_head_features(self) -> None:
        self.add_head_to_head_won()
        self.add_head_to_head_diff()

        self.add_surface_head_to_head_won()
        self.add_surface_head_to_head_diff()

    def add_head_to_head_won(self) -> defaultdict:
        h2h_dict = defaultdict(lambda: [0, 0])
        player_1_h2h_won, player_2_h2h_won = [], []

        for row in self.df.itertuples():
            player_1_id, player_2_id = row.player_1_id, row.player_2_id
            player_1_won = row.player_1_won

            key, first, second = get_h2h_params(player_1_id,
                                                player_2_id, h2h_dict)

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

    def add_surface_head_to_head_won(self) -> defaultdict:
        surface_h2h_dict = defaultdict(lambda: [[0, 0], [0, 0],
                                                [0, 0], [0, 0]])
        player_1_surface_h2h_won, player_2_surface_h2h_won = [], []

        for row in self.df.itertuples():
            player_1_id, player_2_id = row.player_1_id, row.player_2_id
            player_1_won = row.player_1_won

            key, first, second = get_h2h_params(player_1_id,
                                                player_2_id, surface_h2h_dict)

            surface_idx = get_surface_index_by_row(row)

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

    def add_surface_head_to_head_diff(self) -> None:
        self.df["surface_h2h_diff"] = (self.df["player_1_surface_h2h_won"]
                                    - self.df["player_2_surface_h2h_won"])


class MatchDataEngineering(FeatureEngineeringBase):
    def __init__(self, df: pd.DataFrame, last_n_matches: tuple):
        super().__init__(df)
        self.last_n_matches = last_n_matches

    def apply_feature_engineering(self) -> pd.DataFrame:
        self.add_won_match_data()
        return self.df

    def add_won_match_data(self) -> defaultdict:
        match_dt = defaultdict(lambda: [0, 0]
            + len(self.last_n_matches) * [0])
        # index 0 won, 1 total, then last_n_matches results
        player_1_won_match, player_2_won_match = [], []
        player_1_total_match, player_2_total_match = [], []
        last_won_matches_1, last_won_matches_2 = [], []

        for row in self.df.itertuples():
            player_1_id, player_2_id = row.player_1_id, row.player_2_id
            player_1_won = row.player_1_won

            self.append(match_dt, player_1_id, player_2_id,
                    player_1_won_match, player_2_won_match,
                    player_1_total_match, player_2_total_match,
                    last_won_matches_1, last_won_matches_2)

            self.update_matches_dict(match_dt, player_1_id,
                                     player_2_id, player_1_won)

        self.update_won_match(player_1_won_match, player_2_won_match)
        self.update_total_match(player_1_total_match, player_2_total_match)
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

    def append(self, match_dt: defaultdict, player_1_id: int,
            player_2_id: int,player_1_won_match: List[int],
            player_2_won_match: List[int],player_1_total_match:  List[int],
            player_2_total_match: List[int],
            last_won_matches_1: List[List[int]],
            last_won_matches_2: List[List[int]]) -> None:
        self.append_won_match(match_dt, player_1_id, player_2_id,
                              player_1_won_match, player_2_won_match)

        self.append_total_match(match_dt, player_1_id, player_2_id,
                                player_1_total_match, player_2_total_match)

        self.append_last_won_matches(match_dt, player_1_id, player_2_id,
                                     last_won_matches_1, last_won_matches_2)

    def update_won_match(self, player_1_won_match: List[int],
                         player_2_won_match: List[int]) -> None:
        self.df["player_1_won_match"] = player_1_won_match
        self.df["player_2_won_match"] = player_2_won_match

    def update_total_match(self, player_1_total_match: List[int],
                           player_2_total_match: List[int]) -> None:
        self.df["player_1_total_match"] = player_1_total_match
        self.df["player_2_total_match"] = player_2_total_match

    def append_won_match(self, match_dt: defaultdict, player_1_id: int,
            player_2_id: int, player_1_won_match: List[int],
            player_2_won_match: List[int]) -> None:
        player_1_won_match.append(match_dt[player_1_id][0])
        player_2_won_match.append(match_dt[player_2_id][0])

    def append_total_match(self, match_dt: defaultdict, player_1_id: int,
            player_2_id: int, player_1_total_match: List[int],
            player_2_total_match: List[int]) -> None:
        player_1_total_match.append(match_dt[player_1_id][1])
        player_2_total_match.append(match_dt[player_2_id][1])

    def append_last_won_matches(self, match_dt: defaultdict, player_1_id: int,
                        player_2_id: int, last_won_matches_1: List[list],
                                last_won_matches_2: List[list]):
        curr_data_1, curr_data_2 = [], []
        for match_idx, num in enumerate(self.last_n_matches, start=2):
            match_data = get_last_won_match_data(match_dt, player_1_id,
                                                player_2_id, match_idx)

            curr_data_1.append(match_data[0])
            curr_data_2.append(match_data[1])

        last_won_matches_1.append(curr_data_1)
        last_won_matches_2.append(curr_data_2)

    def update_matches_dict(self, match_dt: defaultdict, player_1_id: int,
                            player_2_id: int, player_1_won: bool) -> None:
        update_match_dict(match_dt, player_1_won,
                          player_1_id, player_2_id,
                          self.last_n_matches)


class MatchFeatureDifferenceEngineering(FeatureEngineeringBase):
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
        for row in self.df.itertuples():
            row_idx = row.Index
            player_1_id, player_2_id = row.player_1_id, row.player_2_id
            player_1_elo, player_2_elo = row.player_1_elo, row.player_2_elo

            for last_n in self.last_n_matches:
                player_1_history = players_elo_history[player_1_id]
                player_2_history = players_elo_history[player_2_id]

                self.set_players_elo_progress(players_elo_history, player_1_history,
                    player_2_history, last_n,
                    player_1_id, player_2_id, row_idx)

            append_players_elo_progress(players_elo_history, player_1_id,
                                        player_2_id, player_1_elo, player_2_elo)

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
            new_progress = player_history[-1] / player_history[0]

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

            HeadToHeadEngineering(self.df).apply_feature_engineering,

            (InGameDataEngineering(self.df, self.last_n_matches)
             .apply_feature_engineering),

            (MatchDataEngineering(self.df, self.last_n_matches)
            .apply_feature_engineering),

            (MatchFeatureDifferenceEngineering(self.df, self.last_n_matches)
             .apply_feature_engineering),

            (WinRatioEngineering(self.df, self.last_n_matches)
             .apply_feature_engineering),

            (EloEngineering(self.df, self.last_n_matches)
             .apply_feature_engineering)
        ]

    def apply_feature_engineering(self) -> pd.DataFrame:
        logger.info("Applying feature engineering")

        for step in self.feature_engineering_steps:
            self.df = step()

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
    print(list(df.columns))
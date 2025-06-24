from typing import List, Iterable
from collections import namedtuple, defaultdict

import pandas as pd

from utils.dataframe import read_final_csv
from utils.feature_helpers import (
    get_h2h_params,
    get_surface_index_by_row
)

EXCLUDED_FEATURES = [
    "_id", "_seed", "_ioc", "_ace", "_df", "_svpt", "_1stIn", "_1stWon",
    "_2ndWon", "_SvGms", "_bpSaved", "_bpFaced", "_was_seeded",
    "h2h_won"
]

class Player:
    def __init__(self, row: Iterable, column_names: List[str], num: int=1):
        self.row = row
        self.column_names = column_names
        self.num = num

        self.column_names = self.get_new_column_names()
        PlayerData = self.get_player_data_instance()

        data = [getattr(row, col) for col in self.column_names]
        self.player_data = PlayerData(*data)

    def get_new_column_names(self):
        column_names = (
            [col for col in self.column_names
                    if col.startswith(f"player_{self.num}")
             and not any(
                [feat for feat in EXCLUDED_FEATURES if col.endswith(feat)]
            )
             and "entry" not in col and col != f"player_{self.num}_won"
             ]
        )
        return column_names

    def get_player_data_instance(self):
        PlayerData = namedtuple("PlayerData",
                [col.replace(f"player_{self.num}", "player")
                        for col in self.column_names])
        return PlayerData


def get_player_data_dict(df: pd.DataFrame) -> dict:
    player_data_dict = {}
    column_names = list(df.columns)

    for row in df[::-1].itertuples():
        player_1_id, player_2_id = row.player_1_id, row.player_2_id

        if player_1_id not in player_data_dict:
            player_data_dict[player_1_id] = Player(row, column_names)
        if player_2_id not in player_data_dict:
            player_data_dict[player_2_id] = Player(row, column_names, 2)

    return player_data_dict


def get_head_to_head_dict(df: pd.DataFrame
                          ) -> defaultdict[int, List[int]]:
    h2h_dict = defaultdict(lambda: [0, 0])

    for row in df.itertuples():
        player_1_id, player_2_id = row.player_1_id, row.player_2_id
        player_1_won = row.player_1_won

        key, first, second = get_h2h_params(player_1_id,
                                            player_2_id, h2h_dict)

        if player_1_won:
            h2h_dict[key][first] += 1
        else:
            h2h_dict[key][second] += 1

    return h2h_dict


def get_surface_head_to_head_dict(df: pd.DataFrame
                                   ) -> defaultdict[int, List[List[int]]]:
    surface_h2h_dict = defaultdict(lambda: [[0, 0], [0, 0],
                                                [0, 0], [0, 0]])
    for row in df.itertuples():
        player_1_id, player_2_id = row.player_1_id, row.player_2_id
        player_1_won = row.player_1_won

        key, first, second = get_h2h_params(player_1_id,
                                            player_2_id, surface_h2h_dict)

        surface_idx = get_surface_index_by_row(row)

        if player_1_won:
            surface_h2h_dict[key][surface_idx][first] += 1
        else:
            surface_h2h_dict[key][surface_idx][second] += 1

    return surface_h2h_dict


BOOSTING_DF = read_final_csv("boosting_model")
PLAYER_DATA_DICT = get_player_data_dict(BOOSTING_DF)

H2H_DICT = get_head_to_head_dict(BOOSTING_DF)
SURFACE_H2H_DICT = get_surface_head_to_head_dict(BOOSTING_DF)


if __name__ == '__main__':
    chosen_player = PLAYER_DATA_DICT[101142]
    print(chosen_player.player_data)
    print(len(chosen_player.player_data))

    print(list(H2H_DICT.items())[:5])
    print(list(SURFACE_H2H_DICT.items())[:5])
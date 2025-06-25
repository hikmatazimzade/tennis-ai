from typing import List, Iterable, Tuple
from collections import defaultdict

import pandas as pd

from utils.dataframe import read_final_csv
from utils.feature_helpers import (
    get_h2h_params,
    get_surface_index_by_row,
    get_surface_name_by_row
)

EXCLUDED_FEATURES = [
    "_id", "_seed", "_ioc", "_ace", "_df", "_svpt", "_1stIn", "_1stWon",
    "_2ndWon", "_SvGms", "_bpSaved", "_bpFaced", "_was_seeded",
    "h2h_won"
]

class Player:
    def __init__(self, row: Iterable, num: int=1):
        self.row = row
        self.num = num

        if num == 1: self.column_names = PLAYER_1_COLUMNS
        else: self.column_names = PLAYER_2_COLUMNS

        self.set_player_attributes()

    def set_player_attributes(self):
        for col in self.column_names:
            new_col = col.replace(f"player_{self.num}", "player")
            setattr(self, new_col, getattr(self.row, col))

        return None

    def __str__(self):
        return f"{self.player_name}: {self.player_win_ratio}"


def get_player_data_dict(df: pd.DataFrame) -> dict:
    player_data_dict = {}

    for row in df[::-1].itertuples():
        player_1_id, player_2_id = row.player_1_id, row.player_2_id

        if player_1_id not in player_data_dict:
            player_data_dict[player_1_id] = Player(row)
        if player_2_id not in player_data_dict:
            player_data_dict[player_2_id] = Player(row, 2)

    return player_data_dict


def set_surface_attributes(player_surface_columns: List[str], row: Iterable,
                           player: Player, num: int=1) -> None:
    surface_name = get_surface_name_by_row(row)
    for col in player_surface_columns:
        new_col = f"{col}_{surface_name}"
        new_col = new_col.replace(f"player_{num}", "player")

        row_val = getattr(row, col)

        if not hasattr(player, new_col):
            setattr(player, new_col, row_val)


def add_surface_attributes(df: pd.DataFrame) -> None:
    for row in df[::-1].itertuples():
        player_1_id, player_2_id = row.player_1_id, row.player_2_id
        player_1 = PLAYER_DATA_DICT[player_1_id]
        player_2 = PLAYER_DATA_DICT[player_2_id]

        set_surface_attributes(PLAYER_1_SURFACE_COLUMNS, row, player_1)
        set_surface_attributes(PLAYER_2_SURFACE_COLUMNS, row, player_2, 2)


def get_player_column_names(column_names: List[str],
                            num: int=1) -> List[str]:
    player_column_names = (
        [col for col in column_names
         if col.startswith(f"player_{num}")
         and not any(
            [feat for feat in EXCLUDED_FEATURES if col.endswith(feat)]
        )
         and "entry" not in col and col != f"player_{num}_won"
         ]
    )
    return player_column_names


def get_final_player_columns(PLAYER_1_ALL_COLUMNS: List[str],
                             PLAYER_2_ALL_COLUMNS: List[str]
    ) -> Tuple[List[str], ...]:
    PLAYER_1_COLUMNS = [col for col in PLAYER_1_ALL_COLUMNS
                        if "surface" not in col]
    PLAYER_2_COLUMNS = [col for col in PLAYER_2_ALL_COLUMNS
                        if "surface" not in col]

    PLAYER_1_SURFACE_COLUMNS = [col for col in PLAYER_1_ALL_COLUMNS
                                if "surface" in col]
    PLAYER_2_SURFACE_COLUMNS = [col for col in PLAYER_2_ALL_COLUMNS
                                if "surface" in col]
    return (
        PLAYER_1_COLUMNS, PLAYER_2_COLUMNS,
        PLAYER_1_SURFACE_COLUMNS, PLAYER_2_SURFACE_COLUMNS
    )


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
COLUMN_NAMES = list(BOOSTING_DF.columns)

PLAYER_1_ALL_COLUMNS = get_player_column_names(COLUMN_NAMES, 1)
PLAYER_2_ALL_COLUMNS = get_player_column_names(COLUMN_NAMES, 2)

(
    PLAYER_1_COLUMNS,
    PLAYER_2_COLUMNS,
    PLAYER_1_SURFACE_COLUMNS,
    PLAYER_2_SURFACE_COLUMNS,
) = get_final_player_columns(PLAYER_1_ALL_COLUMNS, PLAYER_2_ALL_COLUMNS)

PLAYER_DATA_DICT = get_player_data_dict(BOOSTING_DF)
add_surface_attributes(BOOSTING_DF)

H2H_DICT = get_head_to_head_dict(BOOSTING_DF)
SURFACE_H2H_DICT = get_surface_head_to_head_dict(BOOSTING_DF)


if __name__ == '__main__':
    chosen_player = PLAYER_DATA_DICT[101142]
    print(chosen_player)
    chosen_dict = chosen_player.__dict__
    del chosen_dict["row"]
    del chosen_dict["column_names"]
    del chosen_dict["num"]

    print(chosen_dict)

    print(list(H2H_DICT.items())[:5])
    print(list(SURFACE_H2H_DICT.items())[:5])
from typing import List, Iterable, Tuple

import pandas as pd

from utils.feature_helpers import (
    get_surface_name_by_row,
)

EXCLUDED_FEATURES = [
    "_id", "_seed", "_ioc", "_ace", "_df", "_svpt", "_1stIn", "_1stWon",
    "_2ndWon", "_SvGms", "_bpSaved", "_bpFaced", "_was_seeded",
    "h2h_won"
]

class Player:
    def __init__(self, row: Iterable, column_names: List[str], num: int=1):
        self.row = row
        self.num = num

        self.column_names = column_names
        self.set_player_attributes()

    def set_player_attributes(self):
        for col in self.column_names:
            new_col = col.replace(f"player_{self.num}", "player")
            setattr(self, new_col, getattr(self.row, col))

        return None

    def __str__(self):
        return f"{self.player_name}: {self.player_win_ratio}"


def get_player_data_dict(df: pd.DataFrame, player_1_columns: List[str],
                         player_2_columns: List[str]) -> dict:
    player_data_dict = {}

    for row in df[::-1].itertuples():
        player_1_id, player_2_id = row.player_1_id, row.player_2_id

        if player_1_id not in player_data_dict:
            player_data_dict[player_1_id] = Player(row, player_1_columns)
        if player_2_id not in player_data_dict:
            player_data_dict[player_2_id] = Player(row, player_2_columns, 2)

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


def add_surface_attributes(df: pd.DataFrame, player_data_dict: dict,
        player_1_surface_columns: List[str],
        player_2_surface_columns: List[str]) -> None:
    for row in df[::-1].itertuples():
        player_1_id, player_2_id = row.player_1_id, row.player_2_id
        player_1 = player_data_dict[player_1_id]
        player_2 = player_data_dict[player_2_id]

        set_surface_attributes(player_1_surface_columns, row, player_1)
        set_surface_attributes(player_2_surface_columns, row, player_2, 2)


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
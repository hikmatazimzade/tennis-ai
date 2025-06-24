from typing import List, Iterable
from collections import namedtuple

import pandas as pd

from utils.dataframe import read_final_csv

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


def get_boosting_df(file_name: str):
    boosting_df = pd.read_csv(file_name, index_col=0)
    return boosting_df


def get_player_data_dict(model: str="boosting_model") -> dict:
    boosting_df = read_final_csv(model)
    player_data_dict = {}
    column_names = list(boosting_df.columns)

    for row in boosting_df[::-1].itertuples():
        player_1_id, player_2_id = row.player_1_id, row.player_2_id

        if player_1_id not in player_data_dict:
            player_data_dict[player_1_id] = Player(row, column_names)
        if player_2_id not in player_data_dict:
            player_data_dict[player_2_id] = Player(row, column_names, 2)

    return player_data_dict

PLAYER_DATA_DICT = get_player_data_dict()


if __name__ == '__main__':
    chosen_player = PLAYER_DATA_DICT[101142]
    print(chosen_player.player_data)
    print(len(chosen_player.player_data))
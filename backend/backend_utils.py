from typing import List, Iterable
from collections import namedtuple

import pandas as pd

from config import ROOT_DIR

BOOSTING_CSV = f"{ROOT_DIR}/data/atp_matches_final_boosting_model.csv"
EXCLUDED_FEATURES = [
    "_id", "_seed", "_ioc", "_ace", "_df", "_svpt", "_1stIn", "_1stWon",
    "_2ndWon", "_SvGms", "_bpSaved", "_bpFaced", "_was_seeded"
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


def get_boosting_df(file_name: str=BOOSTING_CSV):
    boosting_df = pd.read_csv(file_name, index_col=0)

    return boosting_df


def get_player_data_dict(boosting_df: pd.DataFrame) -> dict:
    player_data_dict = {}
    column_names = list(boosting_df.columns)

    for row in boosting_df.itertuples():
        player_1_id, player_2_id = row.player_1_id, row.player_2_id

        if player_1_id not in player_data_dict:
            player_data_dict[player_1_id] = Player(row, column_names)
        if player_2_id not in player_data_dict:
            player_data_dict[player_2_id] = Player(row, column_names, 2)

    return player_data_dict


if __name__ == '__main__':
    boosting_df = get_boosting_df()
    player_data_dict = get_player_data_dict(boosting_df)

    chosen_player = player_data_dict[101142]
    print(chosen_player.player_data)
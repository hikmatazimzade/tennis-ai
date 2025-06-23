from typing import List, Union
from pprint import pprint

import pandas as pd

from config import ROOT_DIR

BOOSTING_CSV = f"{ROOT_DIR}/data/atp_matches_final_boosting_model.csv"


def get_boosting_df(file_name: str=BOOSTING_CSV):
    boosting_df = pd.read_csv(file_name, index_col=0)
    pprint(list(boosting_df.columns))

    return boosting_df


def get_player_data_dict(boosting_df: pd.DataFrame) -> dict:
    player_data_dict = {}
    for row in boosting_df.itertuples():
        player_1_id, player_2_id = row.player_1_id, row.player_2_id
        if player_1_id not in player_data_dict:
            player_data_dict[player_1_id] = row[1:]
        if player_2_id not in player_data_dict:
            player_data_dict[player_2_id] = row[1:]

    return player_data_dict


if __name__ == '__main__':
    boosting_df = get_boosting_df()
    player_data_dict = get_player_data_dict(boosting_df)

    print(player_data_dict[101142])
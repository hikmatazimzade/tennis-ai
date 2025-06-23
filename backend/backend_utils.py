from typing import List, Union
from pprint import pprint

import pandas as pd

from config import ROOT_DIR

BOOSTING_CSV = f"{ROOT_DIR}/data/atp_matches_final_boosting_model.csv"


def get_csv_rows(file_name: str=BOOSTING_CSV):
    df = pd.read_csv(file_name, index_col=0)
    pprint(list(df.columns))

    return df.values.tolist()


def get_player_data_dict(csv_rows: List[Union[int, float, str,
                    bool]]) -> dict:
    player_data_dict = {}
    for row in csv_rows[::-1]:
        player_1_id, player_2_id = row[0], row[29]
        if player_1_id not in player_data_dict:
            player_data_dict[player_1_id] = row[1:]
        if player_2_id not in player_data_dict:
            player_data_dict[player_2_id] = row[1:]

    return player_data_dict


if __name__ == '__main__':
    csv_rows = get_csv_rows()
    player_data_dict = get_player_data_dict(csv_rows)

    print(player_data_dict[101142])
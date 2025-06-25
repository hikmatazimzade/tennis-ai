from backend.backend_utils import (
    get_player_column_names,
    get_final_player_columns,
    get_player_data_dict,
    add_surface_attributes
)

from utils.dataframe import (
    read_final_csv,
    delete_columns
)

from utils.feature_helpers import (
    get_head_to_head_dict,
    get_surface_head_to_head_dict,
)


LAST_N_MATCHES = [5, 10, 20, 50]

BOOSTING_DF = read_final_csv("boosting_model")
COLUMN_NAMES = list(BOOSTING_DF.columns)

PREDICTION_DF = delete_columns(BOOSTING_DF, LAST_N_MATCHES)
PREDICTION_COLUMNS = list(PREDICTION_DF.columns)

PLAYER_1_ALL_COLUMNS = get_player_column_names(COLUMN_NAMES, 1)
PLAYER_2_ALL_COLUMNS = get_player_column_names(COLUMN_NAMES, 2)

(
    PLAYER_1_COLUMNS,
    PLAYER_2_COLUMNS,
    PLAYER_1_SURFACE_COLUMNS,
    PLAYER_2_SURFACE_COLUMNS,
) = get_final_player_columns(PLAYER_1_ALL_COLUMNS, PLAYER_2_ALL_COLUMNS)

PLAYER_DATA_DICT = get_player_data_dict(BOOSTING_DF,
                                        PLAYER_1_COLUMNS, PLAYER_2_COLUMNS)
add_surface_attributes(BOOSTING_DF, PLAYER_DATA_DICT,
                       PLAYER_1_SURFACE_COLUMNS, PLAYER_2_SURFACE_COLUMNS)

H2H_DICT = get_head_to_head_dict(BOOSTING_DF)
SURFACE_H2H_DICT = get_surface_head_to_head_dict(BOOSTING_DF)


if __name__ == '__main__':
    chosen_player = PLAYER_DATA_DICT[101142]
    print(chosen_player)
    chosen_dict = chosen_player.__dict__
    print(len(chosen_dict.keys()))

    del chosen_dict["row"]
    del chosen_dict["column_names"]
    del chosen_dict["num"]

    print(chosen_dict)

    print(list(H2H_DICT.items())[:5])
    print(list(SURFACE_H2H_DICT.items())[:5])
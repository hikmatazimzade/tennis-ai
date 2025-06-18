import os
from typing import List, Union, Optional
from secrets import choice

import pandas as pd
from pandas import DataFrame

from config import ROOT_DIR
from utils.logger import get_logger
from data_processing.random_forest import CleanRandomForestDf
from data_processing.xgboost import CleanXGBoostDf
from data_processing.catboost import CleanCatBoost

from data_processing.feature_engineering import FeatureEngineeringDf

logger = get_logger("utils.dataframe")


def get_cleaner(model: str) -> Union[type[CleanRandomForestDf],
                                    type[CleanXGBoostDf],
                                    type[CleanCatBoost]]:
    if model == "random_forest":
        return CleanRandomForestDf
    elif model == "xgboost":
        return CleanXGBoostDf
    elif model == "catboost":
        return CleanCatBoost


def get_final_path(model: str) -> str:
    final_path = os.path.join(ROOT_DIR, "data",
                              f"atp_matches_final_{model}.csv")
    return final_path


def save_final_dataframe(model: str) -> None:
    final_dataframe = get_final_dataframe(model)
    final_path = get_final_path(model)

    logger.info(f"Successfully saved {model} model to {final_path}!")
    final_dataframe.to_csv(final_path)


def read_final_csv(model: str) -> Optional[DataFrame]:
    final_path = get_final_path(model)
    if not os.path.exists(final_path):
        raise FileNotFoundError(f"Final csv file for {model} not found!")

    return pd.read_csv(final_path)


def get_final_dataframe(model: str) -> DataFrame:
    cleaner = get_cleaner(model)()
    cleaner.clean()
    df = shuffle_winner_loser_data(cleaner.df)

    feature_engineering = FeatureEngineeringDf(df)
    df = feature_engineering.apply_feature_engineering()

    return df


def shuffle_winner_loser_data(df: DataFrame) -> DataFrame:
    winner_cols = get_winner_cols(df)
    loser_cols = get_loser_cols(df)
    remaining_cols = get_remaining_cols(df)

    winner_data = get_df_list_by_col_names(df, winner_cols)
    loser_data = get_df_list_by_col_names(df, loser_cols)
    remaining_data = get_df_list_by_col_names(df, remaining_cols)

    remaining_cols.append("player_1_won")
    winner_cols = [w.replace("winner_", "player_1_") for w in winner_cols]
    loser_cols = [l.replace("loser_", "player_2_") for l in loser_cols]


    col_names = winner_cols + loser_cols + remaining_cols

    players_data = get_players_data(winner_data, loser_data, remaining_data,
                     col_names)

    return players_data


def get_players_data(winner_data: list, loser_data: list,
                    remaining_data: list, col_names: list) -> DataFrame:
    new_list = []
    one, zero = 0, 0
    for winner, loser, remaining in zip(
            winner_data, loser_data, remaining_data
    ):
        random_win = bool(choice(range(0, 2)))
        remaining.append(random_win)

        if random_win:
            new_list.append(winner + loser + remaining)
            one += 1

        else:
            new_list.append(loser + winner + remaining)
            zero += 1

    logger.info(f"{one} winners assigned to player 1")
    logger.info(f"{zero} winners assigned to player 2")

    return DataFrame(new_list, columns=col_names)


def get_df_list_by_col_names(df: DataFrame, column_names: list) -> List[list]:
    return df[column_names].to_numpy().tolist()


def get_winner_cols(df: DataFrame) -> List[str]:
    return [d for d in df if d.startswith("winner_")]


def get_loser_cols(df: DataFrame) -> List[str]:
    return [d for d in df if d.startswith("loser_")]


def get_remaining_cols(df: DataFrame) -> List[str]:
    return [d for d in df if not d.startswith("winner_") and
            not d.startswith("loser_")]


def get_entry_columns_to_delete() -> List[str]:
    return ["player_1_entry_ITF", "player_1_entry_UP",
    "player_1_entry_W", "player_2_entry_ITF", "player_2_entry_UP",
    "player_2_entry_W"]


def get_player_numerical_columns_to_delete() -> List[str]:
    return ["player_1_surface_elo", "player_2_surface_elo",
            "player_1_elo", "player_2_elo", "player_1_age", "player_2_age",
            "player_1_ht", "player_2_ht", "player_1_rank_points",
            "player_2_rank_points", "player_1_rank", "player_2_rank",
            "player_1_seed", "player_2_seed", "player_1_win_ratio",
            "player_2_win_ratio", "player_1_h2h_won", "player_2_h2h_won",
            "player_1_won_match", "player_2_won_match",
            "player_1_total_match", "player_2_total_match"]


def get_columns_with_last_n_matches_to_delete(
        last_n_matches: List[int]) -> List[str]:
    cols = []
    cols.extend([f"player_1_last_{num}_win_ratio" for num in last_n_matches])
    cols.extend([f"player_2_last_{num}_win_ratio" for num in last_n_matches])
    cols.extend([f"player_1_last_{num}_match_won" for num in last_n_matches])
    cols.extend([f"player_2_last_{num}_match_won" for num in last_n_matches])
    return cols


def get_in_game_columns_to_delete() -> List[str]:
    in_game_columns = [
            "ace", "df", "svpt", "1stIn",
            "1stWon", "2ndWon", "SvGms",
            "bpSaved", "bpFaced"
    ]

    columns_to_delete = []
    for game_column in in_game_columns:
        for player in ["player_1", "player_2"]:
            columns_to_delete.append(f"{player}_{game_column}")
            columns_to_delete.append(f"{player}_{game_column}_total")

            for last in (5, 10, 20, 50):
                columns_to_delete.append(f"{player}_{game_column}_"
                                         f"last_{last}")
                columns_to_delete.append(f"{player}_{game_column}_"
                                         f"last_{last}_surface")

    return columns_to_delete


def delete_columns(df: DataFrame,
                            last_n_matches: List[int]) -> DataFrame:
    entry_columns = get_entry_columns_to_delete()
    numerical_columns = get_player_numerical_columns_to_delete()

    in_game_columns = get_in_game_columns_to_delete()
    last_n_matches_columns = get_columns_with_last_n_matches_to_delete(
        last_n_matches)

    columns_to_remove = (
            ["player_1_was_seeded", "player_2_was_seeded", "seed_diff"]
            + ["Unnamed: 0", "tourney_level_O"]
                + ["player_1_id", "player_2_id"]
            + ["player_1_surface_h2h_won", "player_2_surface_h2h_won"]
                + entry_columns + numerical_columns + last_n_matches_columns
                + in_game_columns)
    df = df.drop(columns=[column for column in columns_to_remove],
                 errors="ignore")
    return df


if __name__ == '__main__':
    models = ("random_forest", "catboost", "xgboost")
    for model in models:
        save_final_dataframe(model)

    # df = get_final_dataframe("random_forest")
    # print(df.columns)
from typing import List
from secrets import choice

from pandas import DataFrame

from utils.logger import get_logger
from training.random_forest import CleanRandomForestDf
from data_processing.feature_engineering import FeatureEngineeringDf

logger = get_logger("utils.dataframe")


def get_final_dataframe(model: str) -> DataFrame:
    if model == "random_forest":
        cleaner = CleanRandomForestDf()
    cleaner.clean()
    df = shuffle_winner_loser_data(cleaner.df)

    feature_engineering = FeatureEngineeringDf(df)
    # df = feature_engineering.apply_feature_engineering()

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


if __name__ == '__main__':
    df = get_final_dataframe("random_forest")
    print(df.columns)
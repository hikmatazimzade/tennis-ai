from abc import ABC, abstractmethod
from typing import Tuple

import pandas as pd

from utils.logger import get_logger

logger = get_logger("data_processing.feature_engineering")


class FeatureEngineeringDf(ABC):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def apply_feature_engineering(self) -> pd.DataFrame:
        self.add_rank_diff()
        self.add_rank_points_diff()
        return self.df

    def add_rank_diff(self) -> None:
        self.df["rank_diff"] = (self.df["player_1_rank"]
                            - self.df["player_2_rank"])

    def add_rank_points_diff(self) -> None:
        self.df["rank_points_diff"] = (self.df["player_1_rank_points"]
                                       - self.df["player_1_rank_points"])


if __name__ == '__main__':
    from training.random_forest import CleanRandomForestDf
    from utils.dataframe import get_shuffled_dataframe

    cleaner = CleanRandomForestDf()
    cleaner.clean()

    df = cleaner.df
    shuffled_df = get_shuffled_dataframe(df)

    feature_engineering = FeatureEngineeringDf(shuffled_df)
    feature_engineering.apply_feature_engineering()

    df = feature_engineering.df
    print(df.info())
from abc import ABC, abstractmethod
from typing import Tuple

import pandas as pd

from config import ROOT_DIR
from utils.logger import get_logger

TRAIN_CSV = f"{ROOT_DIR}/data/atp_matches_train.csv"
logger = get_logger("data_processing.feature_engineering")


class FeatureEngineeringDf(ABC):
    def __init__(self, csv_path: str=TRAIN_CSV):
        self.df = pd.read_csv(csv_path)

    def apply_feature_engineering(self) -> pd.DataFrame:
        return self.df
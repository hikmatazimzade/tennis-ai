import pandas as pd

from data_processing.data_preprocessing import CleanDf

from utils.logger import get_logger

logger = get_logger("data_processing.xgboost")


class CleanXGBoostDf(CleanDf):
    def handle_nan_seed_values(self, new_seed: int=64) -> None:
        # Max seed value is 35
        self.df.fillna({"winner_seed": new_seed}, inplace=True)
        self.df.fillna({"loser_seed": new_seed}, inplace=True)

        self.df["winner_was_seeded"] = self.df["winner_seed"] != new_seed
        self.df["loser_was_seeded"] = self.df["loser_seed"] != new_seed

    def handle_winner_loser_ioc_values(self) -> None:
        stacked = self.df[["winner_ioc", "loser_ioc"]].stack()
        codes, uniques = pd.factorize(stacked)
        self.df[["winner_ioc", "loser_ioc"]] = codes.reshape(-1, 2)


if __name__ == '__main__':
    clean_xgboost_df = CleanXGBoostDf()
    clean_xgboost_df.clean()
    print(clean_xgboost_df.df.info())
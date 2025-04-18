from data_processing.data_preprocessing import CleanDf

from utils.logger import get_logger

logger = get_logger("training.random_forest")


class CleanRandomForestDf(CleanDf):
    def handle_nan_seed_values(self):
        self.df.fillna({"winner_seed": 999}, inplace=True)
        self.df.fillna({"loser_seed": 999}, inplace=True)

        self.df["winner_was_seeded"] = self.df["winner_seed"] != 999
        self.df["loser_was_seeded"] = self.df["loser_seed"] != 999


if __name__ == '__main__':
    clean_random_forest_df = CleanRandomForestDf()
    clean_random_forest_df.clean()
    print(clean_random_forest_df.df.info())
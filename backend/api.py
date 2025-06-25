from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from backend.storage import (
    PLAYER_DATA_DICT,
    H2H_DICT,
    SURFACE_H2H_DICT,
    PREDICTION_COLUMNS
)

from backend.backend_utils import Player


app = FastAPI()

TOURNEY_YEAR = 2024
TOURNEY_MONTH = 12
TOURNEY_DAY = 15


class Prediction(BaseModel):
    player_1_id: int
    player_2_id: int
    player_1_entry: str = "ALT"
    player_2_entry: str = "ALT"
    surface: str = "Hard"
    tourney_level: str = "A"
    draw_size: float = 64.0


class PredictionData:
    entry_columns = [
        "ALT", "Alt", "LL", "PR",
        "Q", "SE", "WC"
    ]

    surface_columns = [
        "surface_Carpet", "surface_Clay",
        "surface_Grass", "surface_Hard"
    ]

    tourney_level_columns = [
        'tourney_level_A', 'tourney_level_D', 'tourney_level_F',
        'tourney_level_G', 'tourney_level_M',
    ]

    def __init__(self, player_1: Player, player_2: Player,
                 prediction: Prediction):
        self.player_1 = player_1
        self.player_2 = player_2
        self.prediction = prediction

    def set(self):
        self.set_players_entry_data()
        self.set_players_hand_data()

        self.set_tourney_date()

        self.set_surface_data(self.prediction.surface)
        self.set_tourney_level(self.prediction.tourney_level)

        self.draw_size = self.prediction.draw_size

    def set_players_entry_data(self):
        self.set_player_entry_data(self.prediction.player_1_entry)
        self.set_player_entry_data(self.prediction.player_2_entry, 2)

    def set_players_hand_data(self):
        self.player_1_hand_L = self.player_1.player_hand_L
        self.player_1_hand_R = self.player_1.player_hand_R

        self.player_2_hand_L = self.player_2.player_hand_L
        self.player_2_hand_R = self.player_2.player_hand_R

    def set_tourney_date(self):
        self.tourney_year = TOURNEY_YEAR
        self.tourney_month = TOURNEY_MONTH
        self.tourney_day = TOURNEY_DAY

    def set_player_entry_data(self, entry_name: str, num: int=1):
        for entry_col in self.entry_columns:
            entry_val = True if entry_col == entry_name else False
            setattr(self, f"player_{num}_entry_{entry_col}", entry_val)

    def set_surface_data(self, surface: str) -> None:
        for surface_col in self.surface_columns:
            surface_val = (True if surface_col == f"surface_{surface}"
                           else False)
            setattr(self, surface_col, surface_val)

    def set_tourney_level(self, tourney_level: str) -> None:
        for tourney_col in self.tourney_level_columns:
            tourney_val = (True
                        if tourney_col == f"tourney_level_{tourney_level}"
                        else False)
            setattr(self, tourney_col, tourney_val)


@app.post("/prediction")
def prediction(prediction: Prediction) -> dict:
    player_1 = PLAYER_DATA_DICT[prediction.player_1_id]
    player_2 = PLAYER_DATA_DICT[prediction.player_2_id]

    prediction_data = PredictionData(player_1, player_2, prediction)
    prediction_data.set()

    print(prediction_data.__dict__)

    return {
        "player_1_won": 1,
        "confidence_score": 0.64
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0")
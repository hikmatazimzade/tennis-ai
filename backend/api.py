from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from backend.storage import (
    PLAYER_DATA_DICT,
    H2H_DICT,
    SURFACE_H2H_DICT,
    PREDICTION_COLUMNS
)


app = FastAPI()

TOURNEY_YEAR = 2024
TOURNEY_MONTH = 12
TOURNEY_DAY = 15


class Prediction(BaseModel):
    player_1_entry: str = "ALT"
    player_2_entry: str = "ALT"
    surface: str = "Hard"
    tourney_level: str = "A"
    draw_size: str = 64


@app.post("/prediction")
def prediction(prediction: Prediction) -> dict:
    print(prediction)
    return {
        "player_1_won": 1,
        "confidence_score": 0.64
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0")
from typing import Tuple, List, Dict, Any
from collections import defaultdict
from enum import IntEnum, auto

import pandas as pd


def get_elos(df: pd.DataFrame, K: int) -> Tuple[list, list]:
    elo_rating = defaultdict(lambda: 1500)
    player_1_elos = []
    player_2_elos = []

    for row in df.itertuples(index=False):
        player_1_id, player_2_id = row.player_1_id, row.player_2_id
        player_1_won = row.player_1_won

        append_elos(player_1_elos, player_2_elos, player_1_id,
                    player_2_id, elo_rating)
        update_elo(elo_rating, player_1_won, K, player_1_id, player_2_id)

    return player_1_elos, player_2_elos


class AutoZeroEnum(IntEnum):
    def _generate_next_value_(name, start, count, last_values):
        return count


class Surface(AutoZeroEnum):
    CARPET = auto()
    CLAY = auto()
    GRASS = auto()
    HARD = auto()


def get_surface_index(carpet: bool, clay: bool, grass: bool) -> int:
    if carpet: return Surface.CARPET.value
    if clay: return Surface.CLAY.value
    if grass: return Surface.GRASS.value
    else: return Surface.HARD.value


def get_in_game_data_by_row(row, column: str) -> Tuple[int, int]:
    player_1_column  = f"player_1_{column}"
    player_2_column = f"player_2_{column}"

    player_1_val = getattr(row, player_1_column)
    player_2_val = getattr(row, player_2_column)
    return player_1_val, player_2_val


def get_in_game_dict_over_surfaces() -> defaultdict:
    base_dict = defaultdict(lambda: [[] for _ in range(4)])
    # {"player_id": [carpet_values], [clay_values].....}
    return base_dict


def handle_total_values(row: Tuple[Any, ...], game_column: str,
            total_val_list_1: List[int], total_val_list_2: List[int],
            ply_1_id: int, ply_2_id: int,
            player_total_val_dict: defaultdict) -> None:
    player_1_val, player_2_val = get_in_game_data_by_row(row,
                                                         game_column)

    total_val_list_1.append(player_total_val_dict[ply_1_id])
    total_val_list_2.append(player_total_val_dict[ply_2_id])

    player_total_val_dict[ply_1_id] += player_1_val
    player_total_val_dict[ply_2_id] += player_2_val


def get_last_n_lists(last_len: int) -> tuple[List[List], List[List]]:
    last_n_1 = [[] for _ in range(last_len)]
    last_n_2 = [[] for _ in range(last_len)]
    return last_n_1, last_n_2


def get_last_n_surface_lists(last_len: int) -> tuple[List[List], List[List]]:
    last_n_surface_1 = [[] for _ in range(last_len)]
    last_n_surface_2 = [[] for _ in range(last_len)]
    return last_n_surface_1, last_n_surface_2


def get_last_n_sum(last: int,
            player_list: List[List[List[int]]],
            ply_index_list: List[int]):
    last_n_sum = 0
    for ply_idx, ply in enumerate(player_list):
        curr_ply_index = ply_index_list[ply_idx]
        if len(ply[last]) == 0:
            continue

        elif len(ply[last]) == curr_ply_index:
            last_n_sum += ply[last][-1]

        else:
            last_n_sum += ply[last][curr_ply_index]

    return last_n_sum


class LastN:
    def __init__(self, last_len: int):
        self.last_n_1, self.last_n_2 = get_last_n_lists(last_len)
        self.last_n_surface_1, self.last_n_surface_2 = (
            get_last_n_surface_lists(last_len))


def append_last_n_lists(player_1_list: list, player_2_list: list,
                    last_n: LastN, last: int, ply_1_index_list: List[int],
                    ply_2_index_list: List[int], surface_idx: int,
                    curr_surface_index_1: int, curr_surface_index_2: int):
    last_n_sum_1 = get_last_n_sum(last, player_1_list,
                                  ply_1_index_list)
    last_n_sum_2 = get_last_n_sum(last, player_2_list,
                                  ply_2_index_list)

    last_n.last_n_surface_1[last].append(
        player_1_list[surface_idx][last][curr_surface_index_1]
    )

    last_n.last_n_surface_2[last].append(
        player_2_list[surface_idx][last][curr_surface_index_2]
    )

    last_n.last_n_1[last].append(
        last_n_sum_1
    )

    last_n.last_n_2[last].append(
        last_n_sum_2
    )


def bulk_add(df: pd.DataFrame,
             col_dict: dict[str, List[int]]) -> pd.DataFrame:
    df[list(col_dict.keys())] = pd.DataFrame(col_dict, index=df.index)
    return df


def increase_player_indexes(player_index_dict: Dict[int, List[int]],
                       ply_1_id: int, ply_2_id: int,
                       ply_1_list: List[int],ply_2_list: List[int],
                       surface_idx: int) -> None:
    carpet_idx_1, clay_idx_1, grass_idx_1, hard_idx_1 = ply_1_list[:4]
    carpet_idx_2, clay_idx_2, grass_idx_2, hard_idx_2 = ply_2_list[:4]
    total_idx_1, total_idx_2 = ply_1_list[4], ply_2_list[4]

    carpet_idx_1, clay_idx_1, grass_idx_1, hard_idx_1 = (
        get_new_surface_indexes(carpet_idx_1, clay_idx_1,
                                grass_idx_1, hard_idx_1, surface_idx))

    carpet_idx_2, clay_idx_2, grass_idx_2, hard_idx_2 = (
        get_new_surface_indexes(carpet_idx_2, clay_idx_2,
                                grass_idx_2, hard_idx_2, surface_idx))

    player_index_dict[ply_1_id] = [carpet_idx_1, clay_idx_1,
                                   grass_idx_1, hard_idx_1, total_idx_1 + 1]
    player_index_dict[ply_2_id] = [carpet_idx_2, clay_idx_2,
                                   grass_idx_2, hard_idx_2, total_idx_2 + 1]


def get_new_surface_indexes(carpet_idx: int, clay_idx: int,grass_idx: int,
                hard_idx: int, surface_idx: int) -> Tuple[int, int, int, int]:
    if surface_idx == 0: carpet_idx += 1
    elif surface_idx == 1: clay_idx += 1
    elif surface_idx == 2: grass_idx += 1
    else: hard_idx += 1
    return carpet_idx, clay_idx, grass_idx, hard_idx


def get_surface_index_by_row(row: pd.DataFrame.itertuples) -> int:
    carpet, clay = row.surface_Carpet, row.surface_Clay
    grass, hard = row.surface_Grass, row.surface_Hard
    surface_idx = get_surface_index(carpet, clay, grass)
    return surface_idx


def append_elo_surfaces(player_1_elos: list, player_2_elos: list,
                player_1_id: int, player_2_id: int,
                elo_rating, surface_idx: int) -> None:
    player_1_elos.append(elo_rating[player_1_id][surface_idx])
    player_2_elos.append(elo_rating[player_2_id][surface_idx])


def get_surface_name_by_row(row: pd.DataFrame.itertuples) -> str:
    carpet, clay = row.surface_Carpet, row.surface_Clay
    grass, hard = row.surface_Grass, row.surface_Hard

    if carpet: return "Carpet"
    if clay: return "Clay"
    if grass: return "Grass"
    else: return "Hard"


def update_elo_surface(elo_rating: dict, player_1_won: bool, K: int,
            player_1_id: int, player_2_id: int, surface_idx: int) -> None:
    actual_score_1 = 1 if player_1_won else 0
    actual_score_2 = 1 - actual_score_1

    expected_score_1 = get_expected_score(
        elo_rating[player_1_id] [surface_idx],
        elo_rating[player_2_id][surface_idx]
    )
    expected_score_2 = 1 - expected_score_1

    elo_rating[player_1_id][surface_idx] += K * (actual_score_1
                                                 - expected_score_1)
    elo_rating[player_2_id][surface_idx] += K * (actual_score_2
                                                 - expected_score_2)


def get_elo_surfaces(df: pd.DataFrame, K: int) -> Tuple[list, list]:
    elo_rating = defaultdict(lambda: [1500, 1500, 1500, 1500])
    # carpet, clay, grass, hard

    player_1_elos = []
    player_2_elos = []

    for row in df.itertuples(index=False):
        surface_idx = get_surface_index_by_row(row)

        player_1_id, player_2_id = row.player_1_id, row.player_2_id
        player_1_won = row.player_1_won

        append_elo_surfaces(player_1_elos, player_2_elos, player_1_id,
                    player_2_id, elo_rating, surface_idx)
        update_elo_surface(elo_rating, player_1_won, K, player_1_id,
                           player_2_id, surface_idx)

    return player_1_elos, player_2_elos


def update_elo(elo_rating: dict, player_1_won: bool, K: int, player_1_id: int,
               player_2_id: int) -> None:
    actual_score_1 = 1 if player_1_won else 0
    actual_score_2 = 1 - actual_score_1

    expected_score_1 = get_expected_score(elo_rating[player_1_id],
                                          elo_rating[player_2_id])
    expected_score_2 = 1 - expected_score_1

    elo_rating[player_1_id] += K * (actual_score_1 - expected_score_1)
    elo_rating[player_2_id] += K * (actual_score_2 - expected_score_2)


def get_expected_score(player_1_elo: float, player_2_elo: float) -> float:
    return 1 / (1 + 10 ** ((player_2_elo - player_1_elo) / 400))


def append_elos(player_1_elos: list, player_2_elos: list, player_1_id: int,
                player_2_id: int, elo_rating) -> None:
    player_1_elos.append(elo_rating[player_1_id])
    player_2_elos.append(elo_rating[player_2_id])


def update_match_dict(match_dt: defaultdict, player_1_won: bool,
                      player_1_id: int, player_2_id: int,
                      last_n_matches: tuple) -> None:
    if player_1_won:
        match_dt[player_1_id][0] += 1
        for i, num in enumerate(last_n_matches, start=2):
            match_dt[player_1_id][i] = min(match_dt[player_1_id][i] + 1, num)
            match_dt[player_2_id][i] = max(match_dt[player_2_id][i] - 1, 0)

    else:
        match_dt[player_2_id][0] += 1
        for i, num in enumerate(last_n_matches, start=2):
            match_dt[player_2_id][i] = min(match_dt[player_2_id][i] + 1, num)
            match_dt[player_1_id][i] = max(match_dt[player_1_id][i] - 1, 0)

    match_dt[player_1_id][1] += 1
    match_dt[player_2_id][1] += 1


def append_players_elo_progress(players_elo_history: defaultdict,
                                player_1_id: int, player_2_id: int,
                                player_1_elo: float,
                                player_2_elo: float) -> None:
    append_player_elo_progress(players_elo_history, player_1_id, player_1_elo)
    append_player_elo_progress(players_elo_history, player_2_id, player_2_elo)


def append_player_elo_progress(players_elo_history: defaultdict,
            player_id: int, player_elo: float) -> None:
    players_elo_history[player_id].append(player_elo)


def get_h2h_params(player_1_id: int, player_2_id: int,
                   h2h_dict: defaultdict) -> Tuple[tuple, int, int]:
    if (player_2_id, player_1_id) in h2h_dict:
        key = (player_2_id, player_1_id)
        first, second = 1, 0

    else:
        key = (player_1_id, player_2_id)
        first, second = 0, 1

    return key, first, second


def get_head_to_head_dict(df: pd.DataFrame
                          ) -> defaultdict[int, List[int]]:
    h2h_dict = defaultdict(lambda: [0, 0])

    for row in df.itertuples():
        player_1_id, player_2_id = row.player_1_id, row.player_2_id
        player_1_won = row.player_1_won

        key, first, second = get_h2h_params(player_1_id,
                                            player_2_id, h2h_dict)

        if player_1_won:
            h2h_dict[key][first] += 1
        else:
            h2h_dict[key][second] += 1

    return h2h_dict


def get_surface_head_to_head_dict(df: pd.DataFrame
                                   ) -> defaultdict[int, List[List[int]]]:
    surface_h2h_dict = defaultdict(lambda: [[0, 0], [0, 0],
                                                [0, 0], [0, 0]])
    for row in df.itertuples():
        player_1_id, player_2_id = row.player_1_id, row.player_2_id
        player_1_won = row.player_1_won

        key, first, second = get_h2h_params(player_1_id,
                                            player_2_id, surface_h2h_dict)

        surface_idx = get_surface_index_by_row(row)

        if player_1_won:
            surface_h2h_dict[key][surface_idx][first] += 1
        else:
            surface_h2h_dict[key][surface_idx][second] += 1

    return surface_h2h_dict


def get_last_won_match_data(match_dt: defaultdict, player_1_id: int,
        player_2_id: int, match_idx: int) -> Tuple[int, int]:
    return (match_dt[player_1_id][match_idx],
            match_dt[player_2_id][match_idx])
import dots
from minmax import *
from mcts import *
from fastapi import FastAPI, Query, Body
from typing import List, Optional


def return_board(board: List[List[int]], alg: str = None, move: tuple = None, iter_mcts: float = float('+inf'),
                 time_mcts: float = float('+inf'), depth_minmax: int = None, ab: bool = True,
                 player: str = "human"):
    game = dots.DotsAndBoxes(board=board)
    if player == "human":
        if move not in game.get_available_moves():
            return {"board": game.board, "score": game.get_score(), "current_player": "wrong_move"}
        code = game.edge_play(move, True)
        if code == 0:
            return {"board": game.board, "score": game.get_score(), "current_player": "bot"}
        else:
            return {"board": game.board, "score": game.get_score(), "current_player": "human"}
    if player == "bot":
        if alg == "MCTS":
            move = mcts(game, False, 4, iter_mcts, time_mcts)
            code = game.edge_play(move, False)
            if code == 0:
                return {"board": game.board, "score": game.get_score(), "current_player": "human"}
            else:
                return {"board": game.board, "score": game.get_score(), "current_player": "bot"}
        elif alg == "MINMAX":
            move = minmax(game, depth_minmax, False, ab)[1]
            code = game.edge_play(move, False)
            if code == 0:
                return {"board": game.board, "score": game.get_score(), "current_player": "human"}
            else:
                return {"board": game.board, "score": game.get_score(), "current_player": "bot"}
    else:
        return {"board": game.board, "score": game.get_score(), "current_player": "err"}


app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}


@app.put("/play")
def get_board(
    board: List[List[int]] = Body(...),
    alg: str = Query(None),
    move: List[int] = Body(None),
    iter_mcts: float = Query(float('+inf')),
    time_mcts: float = Query(float('+inf')),
    depth_minmax: Optional[int] = Query(None),
    ab: bool = Query(True),
    player: str = Query("human")
):
    return return_board(board, alg, tuple(move), iter_mcts, time_mcts, depth_minmax, ab, player)


@app.get("/reset")
def get_clean_board(size: int = Query(...)):
    game = dots.DotsAndBoxes(size)
    return {"board": game.board, "score": game.get_score()}

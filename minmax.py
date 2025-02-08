import math
import random


def minmax(game, depth, is_maximising, alpha=-1000, beta=1000):
    moves = game.get_available_moves().copy()
    # End node
    if depth == 0 or len(moves) == 0:
        return game.get_score(), None
    if is_maximising:
        value = -1000
        b_move = moves[0]
        for move in moves:
            code = game.edge_play(move, is_maximising)
            if code == 1 or code == 2:  # Gained points - no player change
                v_temp, p_move = minmax(game, depth - 1, is_maximising, alpha, beta)
            elif code == 0:  # Change of player
                v_temp, p_move = minmax(game, depth - 1, not is_maximising, alpha, beta)
            else:
                print("Err")
            # Alpha/beta
            if v_temp > value:
                b_move = p_move
                value = v_temp
            alpha = max(alpha, value)
            if beta <= alpha:
                game.edge_unplay(move, is_maximising)
                break
            game.edge_unplay(move, is_maximising)
        return value, b_move
    else:  # Minimising player
        value = 1000
        b_move = moves[0]
        for move in moves:
            code = game.edge_play(move, is_maximising)
            if code == -1 or code == -2:  # Gained points - no player change
                v_temp, p_move = minmax(game, depth - 1, is_maximising, alpha, beta)
            elif code == 0:  # Change of player
                v_temp, p_move = minmax(game, depth - 1, not is_maximising, alpha, beta)
            else:
                print("Err")
            # Alpha/beta
            if v_temp < value:
                b_move = move
                value = v_temp
            beta = min(beta, value)
            if beta <= alpha:
                game.edge_unplay(move, is_maximising)
                break
            game.edge_unplay(move, is_maximising)
        return value, b_move

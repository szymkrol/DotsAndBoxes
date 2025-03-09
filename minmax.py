def evaluate_move(game, is_maximising, depth, alpha, beta, use_alpha_beta, move_result):
    if move_result in {-2, -1, 1, 2}:  # Gained points - no player change
        return minmax(game, depth - 1, is_maximising, alpha, beta, use_alpha_beta)
    else:  # Change of player
        return minmax(game, depth - 1, not is_maximising, alpha, beta, use_alpha_beta)


def minmax(game, depth, is_maximising, alpha=-1000, beta=1000, use_alpha_beta=True):
    available_moves = game.get_available_moves().copy()
    # End node
    if depth == 0 or len(available_moves) == 0:
        return game.get_score(), None
    if is_maximising:
        best_value = -1000
        best_move = available_moves[0]
        for move in available_moves:
            move_result = game.edge_play(move, is_maximising)
            evaluated_value, evaluated_move = evaluate_move(game, is_maximising, depth, alpha, beta, use_alpha_beta, move_result)
            if evaluated_value > best_value:
                best_move = move
                best_value = evaluated_value
            # Alpha/beta
            if use_alpha_beta:
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    game.edge_unplay(move, is_maximising)
                    break
            game.edge_unplay(move, is_maximising)
        return best_value, best_move
    else:  # Minimising player
        best_value = 1000
        best_move = available_moves[0]
        for move in available_moves:
            move_result = game.edge_play(move, is_maximising)
            evaluated_value, evaluated_move = evaluate_move(game, is_maximising, depth, alpha, beta, use_alpha_beta, move_result)
            if evaluated_value < best_value:
                best_move = move
                best_value = evaluated_value
            # Alpha/beta
            if use_alpha_beta:
                beta = min(beta, best_value)
                if beta <= alpha:
                    game.edge_unplay(move, is_maximising)
                    break
            game.edge_unplay(move, is_maximising)
        return best_value, best_move

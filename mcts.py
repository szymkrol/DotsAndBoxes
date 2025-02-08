import math
import random


def eval_simple(score):
    return -score


def eval_0_1(score):
    if score < 0:
        return 1
    if score >= 0:
        return 0


def play_to_end(game, is_maximising, eval_fun):
    g1 = game.get_copy()
    while g1.get_available_moves():
        code = g1.edge_play(random.choice(g1.get_available_moves()), is_maximising)
        if code == 0:
            is_maximising = not is_maximising
    return eval_fun(g1.get_score())


def count_UCB(sum_of_points, no_of_parent_simulations, no_of_node_simulations, c):
    if no_of_node_simulations == 0:
        return float('inf')
    if no_of_parent_simulations == 0:
        return float('-inf')
    return (sum_of_points / no_of_node_simulations) + c * math.sqrt(
        math.log(no_of_parent_simulations) / no_of_node_simulations)


def get_max_UCB_child(node, tree, eval_const):
    best_child = max(node['children'], key=lambda a: count_UCB(tree[a]['p_sum'], node['no_visits'], tree[a]['no_visits'], eval_const))
    return tree[best_child]


def single_mcts(tree, eval_const):
    node = tree[0]
    # Finding best leaf node
    while node['children']:
        node = get_max_UCB_child(node, tree, eval_const)
    # Adding children to best leaf
    if node['gamestate'].get_available_moves():
        i = len(tree)
        for move in node['gamestate'].get_available_moves():
            g1 = node['gamestate'].get_copy()
            is_maximising = node['is_maximising']
            code = g1.edge_play(move, is_maximising)
            if code == 0:
                is_maximising = not is_maximising
            node['children'].append(i)
            tree.append(
                {'id': i, 'parent': node['id'], 'children': [], 'move_f_parent': move, 'p_sum': 0, 'gamestate': g1,
                 'no_visits': 0, 'is_maximising': is_maximising})
            i += 1
        # Playing best child of best leaf
        best_child = get_max_UCB_child(node, tree, eval_const)
        score = play_to_end(best_child['gamestate'], best_child['is_maximising'], eval_simple)
        best_child['p_sum'] += score
        best_child['no_visits'] += 1
    else:
        score = 0
    # Backpropagation
    while node['parent'] is not None:
        node['p_sum'] += score
        node['no_visits'] += 1
        node = tree[node['parent']]
    # Root update
    node['p_sum'] += score
    node['no_visits'] += 1


def mcts_n(game, no, is_maximising, eval_const):
    tree = [
        {'id': 0, 'parent': None, 'children': [], 'move_f_parent': None, 'p_sum': 0, 'gamestate': game, 'no_visits': 0,
         'is_maximising': is_maximising}]
    for i in range(no):
        single_mcts(tree, eval_const)
    # Find the best node:
    best_move_child = tree[max(tree[0]['children'], key=lambda a: tree[a]['no_visits'])]
    # print(tree[0])
    # for child in tree[0]['children']:
    #     print(tree[child])
    return best_move_child['move_f_parent']

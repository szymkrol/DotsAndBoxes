import dots
from minmax import *
import math
import random
from mcts import *


def play_first_mcts(game, no, c):
    # ujemna punktacja - dla komputera
    while game.get_available_moves():
        while game.get_available_moves():
            game.print_nice_board()
            mv1_x = int(input())
            mv1_y = int(input())
            code = game.edge_play((mv1_x, mv1_y), True)
            if code == 0:
                break
        while game.get_available_moves():
            mv2 = mcts_n(game, no, True, c)
            print(mv2)

            code = game.edge_play(mv2, False)
            if code == 0:
                break
    return game.get_score()


def play_mcts(game, is_maximising, no, c):
    while game.get_available_moves():
        mv2 = mcts_n(game, no, is_maximising, c)
        code = game.edge_play(mv2, is_maximising)
        if code == 0:
            break


def play_first_minmax(game, depth):
    # ujemna punktacja - dla komputera
    while game.get_available_moves():
        while game.get_available_moves():
            game.print_nice_board()
            mv1_x = int(input())
            mv1_y = int(input())
            code = game.edge_play((mv1_x, mv1_y), True)
            if code == 0:
                break
        while game.get_available_moves():
            mv2 = minmax(game, depth, False)[1]
            print(mv2)
            code = game.edge_play(mv2, False)
            if code == 0:
                break
    return game.get_score()


def play_second_minmax(game, depth):
    # ujemna punktacja - dla komputera
    while game.get_available_moves():
        while game.get_available_moves():
            mv2 = minmax(game, depth, False)[1]
            print(mv2)
            code = game.edge_play(mv2, False)
            if code == 0:
                break
        while game.get_available_moves():
            game.print_nice_board()
            mv1_x = int(input())
            mv1_y = int(input())
            code = game.edge_play((mv1_x, mv1_y), True)
            if code == 0:
                break
    return game.get_score()


g = dots.DotsAndBoxes(5)


print(play_first_mcts(g, 5000, 4.1))

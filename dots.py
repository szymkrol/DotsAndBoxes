import copy


def get_neighbouring_faces(coord):
# Function returning coordinates of faces adjacent to an edge on coord
    x, y = coord
    if x % 2 == 0 and y % 2 == 1:
        return (x - 1, y), (x + 1, y)
    elif x % 2 == 1 and y % 2 == 0:
        return (x, y - 1), (x, y + 1)
    else:
        print("Err")


def get_adjacent_edges(coord):
# Function returning four edges adjacent to a given face on coord
    x, y = coord
    return [(x + dx, y + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]


class DotsAndBoxes:
    def __init__(self, size=0, board=None):
        if board is None:  # Creating new game
            self.size = size
            self.actual_size = 2 * size + 1
            self.board = []
            self.score = 0
            self.played_edges = 0
            self.available_moves = []
            for i in range(self.actual_size):
                self.board.append([])
                for j in range(self.actual_size):
                    if i == 0 or i == self.actual_size - 1 or j == 0 or j == self.actual_size - 1 or (
                            i % 2 == 0 and j % 2 == 0):
                        self.board[i].append(9)
                    else:
                        if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                            self.available_moves.append((i, j))
                        self.board[i].append(0)
        else:  # Creating game from existing board
            self.actual_size = len(board)
            self.size = int((self.actual_size - 1)/2)
            self.board = board
            self.score = 0
            self.played_edges = 0
            self.available_moves = []
            for i in range(self.actual_size):
                for j in range(self.actual_size):
                    if self.board[i][j] in [-1, 1]:
                        self.score += self.board[i][j]
                    if self.board[i][j] == 7:
                        self.played_edges += 1
                    else:
                        if not(i == 0 or i == self.actual_size - 1 or j == 0 or j == self.actual_size - 1) and ((i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0)):
                            self.available_moves.append((i, j))

    def print_board(self):
        for row in self.board:
            print(row)

    def print_nice_board(self):
        i = 0
        print(' ', end='')
        for j in range(self.actual_size):
            print(j, end='')
        print()
        for row in self.board:
            print(i, end='')
            for x in row:
                if x == 9:
                    print('#', end='')
                elif x == 1 or x == -1:
                    print('x', end='')
                elif x == 0:
                    print(' ', end='')
                if i % 2 == 0:
                    if x == 7:
                        print('-', end='')
                else:
                    if x == 7:
                        print('|', end='')
            print('')
            i += 1

    def edge_play(self, coord, is_maximising):
        # Function playing edge on given coord
        x, y = coord
        if self.get_board_state(coord) != 0 or coord not in self.available_moves:
            print("Err - invalid move")
            return -7
        else:
            # Place edge on the board
            self.board[x][y] = 7
            self.available_moves.remove(coord)
            self.played_edges += 1

            # Update state of neighbouring faces
            score_change = 0
            for neigh in get_neighbouring_faces(coord):
                x_n, y_n = neigh
                # Check if neighbouring face is not claimed
                if self.get_board_state(neigh) == 0:
                    for edge in get_adjacent_edges(neigh):
                        if self.get_board_state(edge) == 9 or self.get_board_state(edge) == 7:
                            continue
                        else:
                            break
                    else:  # All edges adjacent to neigh are placed - face is being claimed
                        if is_maximising:
                            self.board[x_n][y_n] = 1
                            self.score += 1
                            score_change += 1
                        else:
                            self.board[x_n][y_n] = -1
                            self.score -= 1
                            score_change += -1
            return score_change

    def edge_unplay(self, coord, is_maximising):
        # Method undoing a move on coord
        if self.get_board_state(coord) == 0 or self.get_board_state(coord) == 9 or coord in self.available_moves:
            print("Err - unplay")
            return -7
        else:
            x, y = coord
            self.board[x][y] = 0
            self.available_moves.append(coord)
            self.played_edges -= 1
            score_change = 0
            # Check if there is a change in claimed faces after undoing a move
            for neigh in get_adjacent_edges(coord):
                x_n, y_n = neigh
                if self.get_board_state(neigh) == -1:
                    self.board[x_n][y_n] = 0
                    self.score += 1
                    score_change += 1
                elif self.get_board_state(neigh) == 1:
                    self.board[x_n][y_n] = 0
                    self.score += -1
                    score_change += -1
            return score_change

    def get_board_state(self, coord):
        return self.board[coord[0]][coord[1]]

    def get_score(self):
        return self.score

    def get_available_moves(self):
        return self.available_moves

    def get_copy(self):
        return DotsAndBoxes(self.size, copy.deepcopy(self.board))

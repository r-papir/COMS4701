# https://gamescrafters.berkeley.edu/site-legacy-archive-sp20/games.php?puzzle=8puzzle


class PuzzleState():

    def __init__(self, board, parent=None, move=None, depth=0, cost=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost

    def get_neighbors(self):
        neighbors = []
        blank = board.index(0)
        row, column = blank // 3, blank % 3

        if row > 0: neighbors.append(('Up', blank, blank - 3))
        if row < 2: neighbors.append(('Down', blank, blank + 3))
        if column > 0: neighbors.append(('Left', blank, blank - 1))
        if column < 2: neighbors.append(('Right', blank, blank + 1))

        result = []
        for direction, i, j in neighbors:
            new_board = list(board)
            new_board[i], new_board[j] = new_board[j], new_board[i]
            result.append((direction, tuple(new_board)))

        return result
    
    def __lt__(self, other):
        return self.cost < other.cost

def manhattan_distance(board):
    total = 0
    for i, tile in enumerate(board):
        if tile == 0:
            continue
        goal_row, goal_column = tile // 3, tile % 3
        current_row, current_column = i // 3, i % 3
        total += abs(goal_row - current_row) + abs(goal_column - current_column)
    return total

# for i in row of grid

# for i in column of grid
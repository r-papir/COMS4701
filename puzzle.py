import sys
import time
import resource
from collections import deque
import heapq

Goal_State = (0, 1, 2, 3, 4, 5, 6, 7, 8)

class PuzzleState():
    def __init__(self, board, parent=None, move=None, depth=0, cost=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost

    def get_neighbors(self):
        neighbors = []
        blank = self.board.index(0)
        row, column = blank // 3, blank % 3

        if row > 0: neighbors.append(('Up', blank, blank - 3))
        if row < 2: neighbors.append(('Down', blank, blank + 3))
        if column > 0: neighbors.append(('Left', blank, blank - 1))
        if column < 2: neighbors.append(('Right', blank, blank + 1))

        result = []
        for direction, i, j in neighbors:
            new_board = list(self.board)
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

def reconstruct_path(state):
    moves = []
    while state.parent is not None:
        moves.append(state.move)
        state = state.parent
    return list(reversed(moves))

def bfs(start_board):
    start_state = PuzzleState(start_board)
    frontier = deque([start_state])
    frontier_set = {start_board}
    explored = set()
    nodes_expanded = 0
    max_depth = 0

    while frontier:
        state = frontier.popleft()
        frontier_set.discard(state.board)

        if state.board == Goal_State:
            return state, nodes_expanded, max_depth

        explored.add(state.board)
        nodes_expanded += 1

        for direction, new_board in state.get_neighbors():
            if new_board not in explored and new_board not in frontier_set:
                child = PuzzleState(new_board, parent=state, move=direction, depth=state.depth + 1)
                frontier.append(child)
                frontier_set.add(new_board)
                if child.depth > max_depth:
                    max_depth = child.depth

    return None, nodes_expanded, max_depth

def dfs(start_board):
    start_state = PuzzleState(start_board)
    frontier = [start_state]
    frontier_set = {start_board}
    explored = set()
    nodes_expanded = 0
    max_depth = 0

    while frontier:
        state = frontier.pop()
        frontier_set.discard(state.board)

        if state.board == Goal_State:
            return state, nodes_expanded, max_depth

        explored.add(state.board)
        nodes_expanded += 1

        for direction, new_board in reversed(state.get_neighbors()):
            if new_board not in explored and new_board not in frontier_set:
                child = PuzzleState(new_board, parent=state, move=direction, depth=state.depth + 1)
                frontier.append(child)
                frontier_set.add(new_board)
                if child.depth > max_depth:
                    max_depth = child.depth

    return None, nodes_expanded, max_depth

def aStar(start_board):
    start_state = PuzzleState(start_board, cost=manhattan_distance(start_board))
    frontier = [(start_state.cost, 0, start_state)]
    frontier_dict = {start_board: start_state.cost}
    explored = set()
    nodes_expanded = 0
    max_depth = 0
    counter = 0

    while frontier:
        _, _, state = heapq.heappop(frontier)

        if state.board in explored:
            continue

        if state.board == Goal_State:
            return state, nodes_expanded, max_depth

        explored.add(state.board)
        nodes_expanded += 1

        for direction, new_board in state.get_neighbors():
            if new_board in explored:
                continue

            g = state.depth + 1
            h = manhattan_distance(new_board)
            f = g + h

            if f < frontier_dict.get(new_board, float('inf')):
                counter += 1
                child = PuzzleState(new_board, parent=state, move=direction, depth=g, cost=f)
                heapq.heappush(frontier, (f, counter, child))
                frontier_dict[new_board] = f
                if child.depth > max_depth:
                    max_depth = child.depth

    return None, nodes_expanded, max_depth

def write_output(state, nodes_expanded, max_depth, run_time, ram):
    path = reconstruct_path(state)
    with open('output.txt', 'w') as f:
        f.write(f"path to goal: {path}\n")
        f.write(f"cost of path: {len(path)}\n")
        f.write(f"nodes expanded: {nodes_expanded}\n")
        f.write(f"search depth: {state.depth}\n")
        f.write(f"max search depth: {max_depth}\n")
        f.write(f"running time: {run_time:.8f}\n")
        f.write(f"max ram usage: {ram:.8f}\n")
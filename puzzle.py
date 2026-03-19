# Rachel Papirmeister
# COMS 4701
# Coding HW 1

from __future__ import division
from __future__ import print_function

import sys
import math
import time
import resource
import queue as Q
from collections import deque
import heapq

#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[self.n*i : self.n*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        blank = self.blank_index
        row = blank // self.n
        if row == 0:
            return None
        new_config = list(self.config)
        new_config[blank], new_config[blank - self.n] = new_config[blank - self.n], new_config[blank]
        return PuzzleState(new_config, self.n, parent=self, action="Up", cost=self.cost + 1)
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        blank = self.blank_index
        row = blank // self.n
        if row == self.n - 1:
            return None
        new_config = list(self.config)
        new_config[blank], new_config[blank + self.n] = new_config[blank + self.n], new_config[blank]
        return PuzzleState(new_config, self.n, parent=self, action="Down", cost=self.cost + 1)
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        blank = self.blank_index
        col = blank % self.n
        if col == 0:
            return None
        new_config = list(self.config)
        new_config[blank], new_config[blank - 1] = new_config[blank - 1], new_config[blank]
        return PuzzleState(new_config, self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        blank = self.blank_index
        col = blank % self.n
        if col == self.n - 1:
            return None
        new_config = list(self.config)
        new_config[blank], new_config[blank + 1] = new_config[blank + 1], new_config[blank]
        return PuzzleState(new_config, self.n, parent=self, action="Right", cost=self.cost + 1)
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

    def __lt__(self, other):
        return self.cost < other.cost


# Function that Writes to output.txt
def writeOutput(state, nodes_expanded, max_depth, run_time, ram):
    path = []
    curr = state
    while curr.parent is not None:
        path.append(curr.action)
        curr = curr.parent
    path = list(reversed(path))

    with open('output.txt', 'w') as f:
        f.write(f"path to goal: {path}\n")
        f.write(f"cost of path: {len(path)}\n")
        f.write(f"nodes expanded: {nodes_expanded}\n")
        f.write(f"search depth: {state.cost}\n")
        f.write(f"max search depth: {max_depth}\n")
        f.write(f"running time: {run_time:.8f}\n")
        f.write(f"max ram usage: {ram:.8f}\n")


def bfs_search(initial_state):
    """BFS search"""
    frontier = deque([initial_state])
    frontier_set = {tuple(initial_state.config)}
    explored = set()
    nodes_expanded = 0
    max_depth = 0

    while frontier:
        state = frontier.popleft()
        frontier_set.discard(tuple(state.config))

        if test_goal(state):
            return state, nodes_expanded, max_depth

        explored.add(tuple(state.config))
        nodes_expanded += 1

        for child in state.expand():
            child_key = tuple(child.config)
            if child_key not in explored and child_key not in frontier_set:
                frontier.append(child)
                frontier_set.add(child_key)
                if child.cost > max_depth:
                    max_depth = child.cost

    return None, nodes_expanded, max_depth


def dfs_search(initial_state):
    """DFS search"""
    frontier = [initial_state]
    frontier_set = {tuple(initial_state.config)}
    explored = set()
    nodes_expanded = 0
    max_depth = 0

    while frontier:
        state = frontier.pop()
        frontier_set.discard(tuple(state.config))

        if test_goal(state):
            return state, nodes_expanded, max_depth

        explored.add(tuple(state.config))
        nodes_expanded += 1

        for child in reversed(state.expand()):
            child_key = tuple(child.config)
            if child_key not in explored and child_key not in frontier_set:
                frontier.append(child)
                frontier_set.add(child_key)
                if child.cost > max_depth:
                    max_depth = child.cost

    return None, nodes_expanded, max_depth


def A_star_search(initial_state):
    """A * search"""
    counter = 0
    start_cost = calculate_total_cost(initial_state)
    frontier = [(start_cost, counter, initial_state)]
    frontier_dict = {tuple(initial_state.config): start_cost}
    explored = set()
    nodes_expanded = 0
    max_depth = 0

    while frontier:
        _, _, state = heapq.heappop(frontier)
        state_key = tuple(state.config)

        if state_key in explored:
            continue

        if test_goal(state):
            return state, nodes_expanded, max_depth

        explored.add(state_key)
        nodes_expanded += 1

        for child in state.expand():
            child_key = tuple(child.config)
            if child_key in explored:
                continue

            f = calculate_total_cost(child)

            if f < frontier_dict.get(child_key, float('inf')):
                counter += 1
                child.cost = state.cost + 1  # g(n)
                heapq.heappush(frontier, (f, counter, child))
                frontier_dict[child_key] = f
                if child.cost > max_depth:
                    max_depth = child.cost

    return None, nodes_expanded, max_depth


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    g = state.cost
    h = sum(calculate_manhattan_dist(i, state.config[i], state.n)
            for i in range(len(state.config)) if state.config[i] != 0)
    return g + h


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    current_row, current_col = idx // n, idx % n
    goal_row, goal_col = value // n, value % n
    return abs(current_row - goal_row) + abs(current_col - goal_col)


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    return puzzle_state.config == list(range(puzzle_state.n * puzzle_state.n))


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    start_ram   = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    if   search_mode == "bfs": result = bfs_search(hard_state)
    elif search_mode == "dfs": result = dfs_search(hard_state)
    elif search_mode == "ast": result = A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        return
        
    end_time = time.time()
    run_time = end_time - start_time
    ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram) / (2**20)

    state, nodes_expanded, max_depth = result
    writeOutput(state, nodes_expanded, max_depth, run_time, ram)
    print("Program completed in %.3f second(s)" % run_time)

if __name__ == '__main__':
    main()
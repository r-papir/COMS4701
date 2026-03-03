from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
from collections import deque
import heapq
import resource

#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0, depth=0):
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        
        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.depth    = depth
        self.children = []
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[self.n*i : self.n*(i+1)])

    def move_up(self):
        if self.blank_index < self.n:
            return None
        new_config = list(self.config)
        target = self.blank_index - self.n
        new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index]
        return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost+1, depth=self.depth+1)
      
    def move_down(self):
        if self.blank_index >= self.n * (self.n - 1):
            return None
        new_config = list(self.config)
        target = self.blank_index + self.n
        new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index]
        return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost+1, depth=self.depth+1)
      
    def move_left(self):
        if self.blank_index % self.n == 0:
            return None
        new_config = list(self.config)
        target = self.blank_index - 1
        new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index]
        return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost+1, depth=self.depth+1)

    def move_right(self):
        if (self.blank_index + 1) % self.n == 0:
            return None
        new_config = list(self.config)
        target = self.blank_index + 1
        new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index]
        return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost+1, depth=self.depth+1)
      
    def expand(self):
        """ Generate the child nodes of this node """
        if len(self.children) != 0:
            return self.children
        
        # Order: Up, Down, Left, Right
        possible_moves = [self.move_up(), self.move_down(), self.move_left(), self.move_right()]
        self.children = [state for state in possible_moves if state is not None]
        return self.children

    def __lt__(self, other):
        return self.cost < other.cost

# Function that Writes to output.txt
def writeOutput(state, nodes_expanded, max_depth, ram):
    path = []
    curr = state
    while curr.parent is not None:
        path.append(curr.action)
        curr = curr.parent
    path.reverse()

    with open('output.txt', 'w') as f:
        f.write(f"path_to_goal: {path}\n")
        f.write(f"cost_of_path: {len(path)}\n")
        f.write(f"nodes_expanded: {nodes_expanded}\n")
        f.write(f"search_depth: {state.depth}\n")
        f.write(f"max_search_depth: {max_depth}\n")
        f.write(f"running_time: {time.time() - start_time:.8f}\n")
        f.write(f"max_ram_usage: {ram:.8f}\n")

def bfs_search(initial_state):
    frontier = deque([initial_state])
    frontier_set = {initial_state.config}
    explored = set()
    nodes_expanded = 0
    max_depth = 0

    while frontier:
        state = frontier.popleft()
        frontier_set.remove(state.config)
        explored.add(state.config)

        if test_goal(state):
            writeOutput(state, nodes_expanded, max_depth, get_ram())
            return True

        nodes_expanded += 1
        for child in state.expand():
            if child.config not in explored and child.config not in frontier_set:
                frontier.append(child)
                frontier_set.add(child.config)
                if child.depth > max_depth:
                    max_depth = child.depth
    return False

def dfs_search(initial_state):
    frontier = [initial_state]
    frontier_set = {initial_state.config}
    explored = set()
    nodes_expanded = 0
    max_depth = 0

    while frontier:
        state = frontier.pop()
        frontier_set.remove(state.config)
        explored.add(state.config)

        if test_goal(state):
            writeOutput(state, nodes_expanded, max_depth, get_ram())
            return True

        nodes_expanded += 1
        # Reverse children to maintain UDLR priority in a LIFO stack
        for child in reversed(state.expand()):
            if child.config not in explored and child.config not in frontier_set:
                frontier.append(child)
                frontier_set.add(child.config)
                if child.depth > max_depth:
                    max_depth = child.depth
    return False

def A_star_search(initial_state):
    counter = 0 # Tie-breaker
    start_cost = calculate_total_cost(initial_state)
    frontier = [(start_cost, counter, initial_state)]
    frontier_dict = {initial_state.config: start_cost}
    explored = set()
    nodes_expanded = 0
    max_depth = 0

    while frontier:
        _, _, state = heapq.heappop(frontier)
        if state.config in explored: continue
        
        explored.add(state.config)
        if test_goal(state):
            writeOutput(state, nodes_expanded, max_depth, get_ram())
            return True

        nodes_expanded += 1
        for child in state.expand():
            if child.config not in explored:
                f_cost = child.depth + calculate_total_cost(child)
                if f_cost < frontier_dict.get(child.config, float('inf')):
                    counter += 1
                    frontier_dict[child.config] = f_cost
                    heapq.heappush(frontier, (f_cost, counter, child))
                    if child.depth > max_depth:
                        max_depth = child.depth
    return False

def calculate_total_cost(state):
    """Total Manhattan distance for all tiles"""
    dist = 0
    for idx, value in enumerate(state.config):
        if value != 0:
            dist += calculate_manhattan_dist(idx, value, state.n)
    return dist

def calculate_manhattan_dist(idx, value, n):
    target_row, target_col = value // n, value % n
    curr_row, curr_col = idx // n, idx % n
    return abs(target_row - curr_row) + abs(target_col - curr_col)

def test_goal(puzzle_state):
    return puzzle_state.config == tuple(range(puzzle_state.n**2))

def get_ram():
    # Returns RAM usage in MB
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024

# Main Function
def main():
    global start_time
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = tuple(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")

if __name__ == '__main__':
    main()
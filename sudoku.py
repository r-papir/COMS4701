import sys

ROW = "ABCDEFGHI"
COL = "123456789"

# Each sudoku board is represented as a dictionary with string keys and int values (e.g. my_board['A1'] = 8)

def print_board(board):
    # Helper function to print board in a square
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)

def board_to_string(board):
    # Helper function to convert board dictionary to string for writing
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def get_peers(var):
    # Return all peers of a variable (same row, col, or box)
    row, col = var[0], var[1]
    peers = set()
    for c in COL:
        if c != col:
            peers.add(row + c)
    for r in ROW:
        if r != row:
            peers.add(r + col)
    box_row_start = (ROW.index(row) // 3) * 3
    box_col_start = (int(col) - 1) // 3 * 3
    for r in ROW[box_row_start:box_row_start + 3]:
        for c in COL[box_col_start:box_col_start + 3]:
            if r + c != var:
                peers.add(r + c)
    return peers

PEERS = {ROW[r] + COL[c]: get_peers(ROW[r] + COL[c])
         for r in range(9) for c in range(9)}

def initialize_domains(board):
    # Initialize domains for all variables with constraint propagation
    domains = {}
    for var in board:
        if board[var] == 0:
            domains[var] = set(range(1, 10))
        else:
            domains[var] = {board[var]}
    for var in board:
        if board[var] != 0:
            for peer in PEERS[var]:
                domains[peer].discard(board[var])
    return domains

def select_unassigned_variable(board, domains):
    # MRV heuristic: pick unassigned variable with fewest legal values
    unassigned = [v for v in board if board[v] == 0]
    return min(unassigned, key=lambda v: len(domains[v]))

def forward_checking(board, domains, var, value):
    # Apply forward checking - returns new domains or None if contradiction
    new_domains = {v: set(d) for v, d in domains.items()}
    new_domains[var] = {value}
    for peer in PEERS[var]:
        if board[peer] == 0:
            new_domains[peer].discard(value)
            if len(new_domains[peer]) == 0:
                return None
    return new_domains

def backtrack(board, domains):
    # Recursive backtracking search
    if all(board[v] != 0 for v in board):
        return board
    var = select_unassigned_variable(board, domains)
    for value in sorted(domains[var]):
        new_domains = forward_checking(board, domains, var, value)
        if new_domains is None:
            continue
        board[var] = value
        result = backtrack(board, new_domains)
        if result is not None:
            return result
        board[var] = 0
    return None

def backtracking(board):
    # Takes a board and returns solved board
    domains = initialize_domains(board)
    result = backtrack(board, domains)
    return result if result is not None else board

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv[1]) != 81:
            print("ERROR: Input string must be exactly 81 characters long.")
            exit()

        print(sys.argv[1])
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}

        solved_board = backtracking(board)

        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')
    else:
        print("Usage: python3 sudoku.py <input string>")

    print("Finishing all boards in file.")
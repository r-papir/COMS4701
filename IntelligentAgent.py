'Rachel Papirmeister'
'UNI: rmp2205'

import time
import math
from BaseAI import BaseAI

TIME_LIMIT = 0.18
MAX_DEPTH = 4


class IntelligentAgent(BaseAI):

    def getMove(self, grid):
        self.start_time = time.process_time()
        best_move = None
        best_val = float('-inf')

        for move, new_grid in grid.getAvailableMoves():
            val = self.minimize(new_grid, float('-inf'), float('inf'), depth=1)
            if val > best_val:
                best_val = val
                best_move = move

        return best_move

    def time_up(self):
        return time.process_time() - self.start_time >= TIME_LIMIT

    # ---------- minimax with alpha-beta pruning ----------

    def maximize(self, grid, alpha, beta, depth):
        """MAX NODE: player picks the best move"""
        if self.time_up() or depth >= MAX_DEPTH or not grid.getAvailableMoves():
            return self.evaluate(grid)

        best = float('-inf')
        for _, new_grid in grid.getAvailableMoves():
            val = self.minimize(new_grid, alpha, beta, depth + 1)
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break  # beta cutoff
        return best

    def minimize(self, grid, alpha, beta, depth):
        """
        MIN NODE: computer places a tile adversarially; treat the computer as always picking the worst tile
        in the worst cell (4, probability 0.1) --> this is adjusted for by weighting evaluation by tile probability in expectiminimax
        """
        cells = grid.getAvailableCells()

        if self.time_up() or depth >= MAX_DEPTH or not cells:
            return self.evaluate(grid)

        best = float('inf')

        for tile in [4, 2]:
            for cell in cells:
                new_grid = grid.clone()
                new_grid.setCellValue(cell, tile)
                val = self.maximize(new_grid, alpha, beta, depth + 1)

                # Weight by tile probability to respect expectiminimax principles
                if tile == 2:
                    val *= 0.9
                else:
                    val *= 0.1

                best = min(best, val)
                beta = min(beta, best)
                if beta <= alpha:
                    break  # alpha cutoff
            if beta <= alpha:
                break

        return best

    # ---------- heuristics ----------

    def evaluate(self, grid):
        return (
            1.0 * self.free_cells(grid) +
            1.0 * self.monotonicity(grid) +
            0.5 * self.smoothness(grid) +
            1.0 * self.max_tile_corner(grid)
        )

    def free_cells(self, grid):
        return len(grid.getAvailableCells())

    def monotonicity(self, grid):
        """
        rewards boards where tiles decrease in value along rows and columns
        """
        totals = [0, 0, 0, 0]  # left, right, up, down

        for i in range(4):
            for j in range(3):
                # left-right
                cur = grid.map[i][j]
                nxt = grid.map[i][j + 1]
                if cur and nxt:
                    cur_log = math.log2(cur)
                    nxt_log = math.log2(nxt)
                    if cur_log > nxt_log:
                        totals[0] += nxt_log - cur_log
                    elif nxt_log > cur_log:
                        totals[1] += cur_log - nxt_log

                # up-down
                cur = grid.map[j][i]
                nxt = grid.map[j + 1][i]
                if cur and nxt:
                    cur_log = math.log2(cur)
                    nxt_log = math.log2(nxt)
                    if cur_log > nxt_log:
                        totals[2] += nxt_log - cur_log
                    elif nxt_log > cur_log:
                        totals[3] += cur_log - nxt_log

        return max(totals[0], totals[1]) + max(totals[2], totals[3])

    def smoothness(self, grid):
        """
        Penalizes large differences between adjacent tiles; smoother boards are easier to merge
        """
        penalty = 0
        for i in range(4):
            for j in range(4):
                if grid.map[i][j] == 0:
                    continue
                val = math.log2(grid.map[i][j])
                for di, dj in [(0, 1), (1, 0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < 4 and 0 <= nj < 4 and grid.map[ni][nj] != 0:
                        neighbor = math.log2(grid.map[ni][nj])
                        penalty -= abs(val - neighbor)
        return penalty

    def max_tile_corner(self, grid):
        """
        rewards keeping the max tile in a corner
        """
        max_tile = grid.getMaxTile()
        corners = [
            grid.map[0][0], grid.map[0][3],
            grid.map[3][0], grid.map[3][3]
        ]
        if max_tile in corners:
            return math.log2(max_tile)
        return 0
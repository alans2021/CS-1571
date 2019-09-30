import sys
import search
import csp
from csp import Sudoku
from csp import Sudoku2


def sudokuSolver(grid):

    sudoku = Sudoku2(grid)
    bfs = search.breadth_first_tree_search(sudoku)
    sudoku.display()


if __name__ == '__main__':
    sudokuFiles = ["exampleSudokus-q1.txt"];
    for file in sudokuFiles:
        lines = [line.rstrip('\n') for line in open(file)]
        for i in range(0, len(lines)):
            sudokuSolver(lines[i])
    exit(0)

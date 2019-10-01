import search
from csp import Sudoku2
import time


def sudokuSolver(grid):
    sudoku = Sudoku2(grid)
    f = open("output.txt", "a")

    inittime = time.time()
    info = search.breadth_first_tree_search(sudoku)
    finaltime = time.time()
    solution = sudoku.display(dict(info[0].state))
    f.write("BFS Algorithm Solution For " + grid + ":\n")
    f.write(solution + "\n")
    f.write("Nodes generated: " + str(info[1]) + "; Maximum nodes stored: " + str(info[2]) + "\n")
    f.write("Runtime: " + str(finaltime - inittime) + " seconds\n")
    f.write("\n")

    print("Finished breadth first search")

    inittime = time.time()
    info = search.depth_first_tree_search(sudoku)
    finaltime = time.time()
    solution = sudoku.display(dict(info[0].state))
    f.write("DFS Algorithm Solution For " + grid + ":\n")
    f.write(solution + "\n")
    f.write("Nodes generated: " + str(info[1]) + "; Maximum nodes stored: " + str(info[2]) + "\n")
    f.write("Runtime: " + str(finaltime - inittime) + " seconds\n")
    f.write("\n")
    f.close()

    print("Finished depth first search")


if __name__ == '__main__':
    file = open("output.txt", "w")
    file.close()
    file = "exampleSudokus-q1.txt"
    lines = [line.rstrip('\n') for line in open(file)]
    for i in range(0, len(lines)):
        sudokuSolver(lines[i])
    exit(0)

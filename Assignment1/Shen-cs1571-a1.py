import search
import csp
from csp import Sudoku2
import time

prev = None


def sudokuSolver(grid, algorithm):
    sudoku = Sudoku2(grid)
    f = open("output2.txt", "a")
    global prev
    if prev != grid:
        prev = grid
        # inittime = time.time()
        # info = search.breadth_first_tree_search(sudoku)
        # finaltime = time.time()
        # solution = sudoku.display(dict(info[0].state))
        # f.write("BFS Algorithm Solution For " + grid + ":\n")
        # f.write(solution + "\n")
        # f.write("Nodes generated: " + str(info[1]) + "; Maximum nodes stored: " + str(info[2]) + "\n")
        # f.write("Runtime: " + str(finaltime - inittime) + " seconds\n")
        # f.write("\n")
        #
        # print("Finished breadth first search")
        #
        inittime = time.time()
        info = search.depth_first_tree_search(sudoku)
        info[2] = info[2] + grid.count('.')
        finaltime = time.time()
        solution = sudoku.display(dict(info[0].state))
        f.write("DFS Algorithm Solution For " + grid + ":\n")
        f.write(solution + "\n")
        f.write("Nodes generated: " + str(info[1]) + "; Maximum nodes stored: " + str(info[2]) + "\n")
        f.write("Runtime: " + str(finaltime - inittime) + " seconds\n")
        f.write("\n")

        print("Finished depth first search")

        inittime = time.time()
        result, num = csp.backtracking_search(sudoku, None)
        finaltime = time.time()
        solution = sudoku.display(dict(result))
        f.write("Backtracking Algorithm Solution For " + grid + ":\n")
        f.write(solution + "\n")
        f.write("Assignments made: " + str(num) + "\n")
        f.write("Runtime: " + str(finaltime - inittime) + " seconds\n")
        f.write("\n")

        print("Finished regular backtracking search")

    inittime = time.time()
    result, num = csp.backtracking_search(sudoku, algorithm)
    finaltime = time.time()
    solution = sudoku.display(dict(result))
    f.write(algorithm + " Algorithm Solution For " + grid + ":\n")
    f.write(solution + "\n")
    f.write("Assignments made: " + str(num) + "\n")
    f.write("Runtime: " + str(finaltime - inittime) + " seconds\n")
    f.write("\n")
    f.close()

    print("Finished " + algorithm)


if __name__ == '__main__':
    file = open("output2.txt", "w")
    file.close()
    file = "exampleSudokus-q1.txt"
    algs = ["backtracking-ordered", "backtracking-noOrdering", "backtracking-reverse"]
    lines = [line.rstrip('\n') for line in open(file)]
    for i in range(0, len(lines)):
        for j in range(0, len(algs)):
            sudokuSolver(lines[i], algs[j])
    exit(0)

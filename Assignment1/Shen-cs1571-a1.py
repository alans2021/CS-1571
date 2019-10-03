import search
import csp
from csp import Sudoku2
from csp import CourseScheduling
import time

prev = None


def sudokuSolver(grid, algorithm):
    sudoku = Sudoku2(grid)
    f = open("sudoku.txt", "a")
    global prev
    if prev != grid:
        prev = grid
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
    print(str(finaltime) + " " + str(inittime))
    f.write(algorithm + " Algorithm Solution For " + grid + ":\n")
    f.write(solution + "\n")
    f.write("Assignments made: " + str(num) + "\n")
    f.write("Runtime: " + str(finaltime - inittime) + " seconds\n")
    f.write("\n")
    f.close()

    print("Finished " + algorithm)


def scheduleCourses(filename, slots):
    sections = []
    lines = [line.rstrip('\n') for line in open(filename)]
    for course in lines:
        components = course.split(";")
        course_code = components[0]
        profs = components[5].split(",")
        prof_sections = components[6].split(",")
        if len(components) == 8:
            areas = components[7]
        else:
            areas = ""

        for i in range(0, len(profs)):
            profs[i] = profs[i].strip()
        for i in range(0, len(prof_sections)):
            prof_sections[i] = int(prof_sections[i].strip(), 10)

        index = 1
        for i in range(0, len(profs)):
            prof = profs[i]
            num_sec = prof_sections[i]
            for j in range(0, num_sec):
                string = course_code + "-" + prof + "-" + str(index) + "-" + areas
                sections.append(string)
                index += 1

    schedulingCSP = CourseScheduling(sections, slots)
    result, num = csp.backtracking_search(schedulingCSP, "course-scheduling")
    schedule = schedulingCSP.display(result)
    f = open("Course-Schedule.txt", "w")
    f.write("Course Schedule assuming " + str(slots) + " time slots with mrv heuristics and degree heuristic as "
                                                       "tiebreaker\n")
    f.write(schedule + "\n")
    f.write("\n")

    # result, num = csp.backtracking_search(SchedulingCSP, "course-scheduling-degree")
    # schedule = SchedulingCSP.display(result)
    # f.write("Course Schedule assuming " + str(slots) + " time slots and degree heuristic\n")
    # f.write(schedule + "\n")
    # f.write("\n")
    f.close()


if __name__ == '__main__':
    # file = open("sudoku.txt", "w")
    # file.close()
    # file = "exampleSudokus-q1.txt"
    # algs = ["backtracking-ordered", "backtracking-noOrdering", "backtracking-reverse"]
    # lines = [line.rstrip('\n') for line in open(file)]
    # for i in range(0, len(lines)):
    #     for j in range(0, 3):
    #         sudokuSolver(lines[i], algs[j])

    # test = csp.NQueensCSP(8)
    # test = csp.Sudoku2("...1.13..32.2... ")
    file = "partB-courseList-shortened.txt"
    slots = int(input("Enter number of time slots available\n"))
    # slots = 10
    scheduleCourses(file, slots)
    exit(0)

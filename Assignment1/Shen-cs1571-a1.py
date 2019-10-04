import sys
import search
import csp
import math
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
    f.close()


def findPath(start, end, algorithm):
    # Average human walking speed is 3.1 mph
    # Each degree of latitude is approx. 69 miles apart
    # Each degree of longitude at Pittsburgh is approx. 52.468 miles apart
    goal_index = 0
    elevation_file = "partC-intersections.txt"
    distance_file = "partC-distances.txt"
    intersections = []
    latitude = []
    longitude = []
    elevation = []
    heuristics = dict()

    lines = [line.rstrip('\n') for line in open(elevation_file)]
    for line in lines:
        intersect_info = line.split(",")
        latitude.append(float(intersect_info[2]))
        longitude.append(float(intersect_info[3]))
        elevation.append(float(intersect_info[4]))
        new_intersect = intersect_info[0] + "," + intersect_info[1]
        intersections.append(new_intersect)
        if new_intersect == end:
            goal_index = len(intersections) - 1

    for j in range(0, len(intersections)):
        latDist = (latitude[j] - latitude[goal_index]) * 69
        longDist = (longitude[j] - longitude[goal_index]) * 52.468
        twoDimDist = math.sqrt(latDist**2 + longDist**2)
        elevaDist = (elevation[j] - elevation[goal_index]) * 0.0006213712
        totalDist = math.sqrt(twoDimDist**2 + elevaDist**2)
        heuristics[intersections[j]] = totalDist

    pittsburgh_map = dict()  # First create association of neighbors of each intersection
    for intersect in intersections:
        lines = [line.rstrip('\n') for line in open(distance_file)]
        neighbors = dict()
        for line in lines:
            line_arr = line.split(",")
            intersect1 = line_arr[0] + "," + line_arr[1]
            intersect2 = line_arr[2] + "," + line_arr[3]
            if intersect == intersect1:
                neighbors[intersect2] = float(line_arr[4])
            elif intersect == intersect2:
                neighbors[intersect1] = float(line_arr[4])
        pittsburgh_map[intersect] = neighbors
    pittsburgh_graph = search.GraphProblem(start, end, pittsburgh_map)  # Create graph of pittsburgh
    solution = search.astar_search(pittsburgh_graph, heuristics)
    time = solution.path_cost / 3.1 * 60  # Time in minutes to travel that distance
    output = "," + solution.state + "," + str(time)
    while solution.parent is not None:
        solution = solution.parent
        output = "," + solution.state + output
    print("Result of " + algorithm + " search from " + start + " to " + end + ":")
    print(output[1:])


if __name__ == '__main__':
    # test = sys.argv
    # file = open("sudoku.txt", "w")
    # file.close()
    # file = "exampleSudokus-q1.txt"
    # algs = ["backtracking-ordered", "backtracking-noOrdering", "backtracking-reverse"]
    # lines = [line.rstrip('\n') for line in open(file)]
    # for i in range(0, len(lines)):
    #     for j in range(0, 3):
    #         sudokuSolver(lines[i], algs[j])

    # file = "partB-courseList-shortened.txt"
    # slots = int(input("Enter number of time slots available\n"))
    # scheduleCourses(file, slots)
    findPath("Forbes,Bouquet", "Bigelow,Lytton", "idAstar")
    exit(0)

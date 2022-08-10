# IMPORT LIBRARIES
from utils import *
from timeit import default_timer as timer

def solve_problem(input_directory):

    w, n, x, y, maxlen = read_file(input_directory)

    solution = [[[Bool(f"solution_{i}_{j}_{k}") for k in range(n)] for j in range(maxlen)] for i in range(w)]
    rotation = [Bool(f"rotation_{k}") for k in range(n)]
    print("rotation", rotation)

    start = timer()

    #takes the index of biggest silicon
    biggest_silicon = 0
    for k in range(n):
        if x[biggest_silicon] * y[biggest_silicon] < x[k] * y[k]:
            biggest_silicon = k

    l = min(y) #*TO CHECK*

    solved = False

    while l <= maxlen and solved == False:
        s = Solver()

        # no overlapping
        for j in range(l):
            for i in range(w):
                s.add(at_most_one([solution[i][j][k] for k in range(n)]))

        # puts the silicon with larger area in the bottom left corner
        s.add([And(solution[0][0][biggest_silicon])])

        # makes sure silicons fit
        for k in range(n):
            possible_sols = []
            for i in range(w - x[k] + 1):
                for j in range(l - y[k] + 1):
                    silicons_position = []
                    for ox in range(w):
                        for oy in range(l):
                            if i <= ox < i + x[k] and j <= oy < j + y[k]:
                                silicons_position.append(solution[ox][oy][k])
                            else:
                                silicons_position.append(Not(solution[ox][oy][k]))
                    possible_sols.append(And(silicons_position))

            non_rotated_silicons = And(Not(rotation[k]), And(exactly_one(possible_sols)))
            #s.add(exactly_one(possible_sols))

            possible_sols = []
            for i in range(w - y[k] + 1): #inverted x and y for handling rotation
                for j in range(l - x[k] + 1):
                    silicons_position = []
                    for ox in range(w):
                        for oy in range(l):
                            if i <= ox < i + y[k] and j <= oy < j + x[k]:
                                silicons_position.append(solution[ox][oy][k])
                            else:
                                silicons_position.append(Not(solution[ox][oy][k]))
                    possible_sols.append(And(silicons_position))

            rotated_silicons = And(rotation[k], And(exactly_one(possible_sols)))

            s.add(exactly_one([non_rotated_silicons, rotated_silicons]))

        if s.check() == sat:
            time = timer() - start
            print("model solved with length:", l, "in time: ", time, "s")
            #print(s.model())
            solved = True
        else:
            print("Failed to solve with length : ", l)
            l = l + 1
            #condition to stop

    get_solution(s.model(), solution, w, l, n, maxlen)
    return s.model(), l


def main():
    input_directory = "./instances/ins-1.txt"
    # output_directory = ".\instances\ins-11.txt" #to define when write file
    solve_problem(input_directory)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


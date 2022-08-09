# IMPORT LIBRARIES
from utils import *
from timeit import default_timer as timer

def solve_problem(input_directory):

    w, n, x, y, maxlen = read_file(input_directory)

    solution = [[[Bool(f"solution_{i}_{j}_{k}") for k in range(n)] for j in range(maxlen)] for i in range(w)]

    start = timer()

    #takes the index of biggest silicon
    biggest_silicon = 0
    for k in range(n):
        if x[biggest_silicon] * y[biggest_silicon] < x[k] * y[k]:
            biggest_silicon = k

    l = min(y)

    solved = False
    while l <= maxlen and solved == False:
        s = Solver()
        # no overlapping
        for j in range(l):
            for i in range(w):
                s.add(at_most_one([solution[i][j][k] for k in range(n)]))

        # makes sure silicons fit
        for k in range(n):
            possible_sols = []
            for i in range(w - x[k] + 1):
                for j in range(l - y[k] + 1):
                    circuit = []
                    for ox in range(w):
                        for oy in range(l):
                            if i <= ox < i + x[k] and j <= oy < j + y[k]:
                                circuit.append(solution[ox][oy][k])
                            else:
                                circuit.append(Not(solution[ox][oy][k]))
                    possible_sols.append(And(circuit))
            s.add(exactly_one(possible_sols))

        # puts the silicon with larger area in the bottom left corner
        s.add([And(solution[0][0][biggest_silicon])])

        if s.check() == sat:
            time = timer() - start
            print("model solved with length:", l, "in time: ", time, "s")
            print(s.model())
            solved = True
            print(time)
        else:
            print("Failed to solve with length: ", l)
            l = l + 1

    get_solution(s.model(), solution, w, l, n, maxlen)
    return s.model(), l


def main():
    input_directory = "./instances/ins-1.txt"
    #output_directory = ".\instances\ins-11.txt" #to define when write file
    solve_problem(input_directory)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


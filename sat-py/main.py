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


    sum = 0
    for k in range(n):
        sum += x[k] * y[k]
    l = math.floor(sum / w)


    solved = False
    while l <= maxlen and solved == False:
        solver = Solver()
        # no overlapping
        for j in range(l):
            for i in range(w):
                solver.add(at_most_one([solution[i][j][k] for k in range(n)]))

        # makes sure silicons fit
        for k in range(n):
            possible_sols = []
            for i in range(w - x[k] + 1):
                for j in range(l - y[k] + 1):
                    silicon = []
                    for ox in range(w):
                        for oy in range(l):
                            if i <= ox < i + x[k] and j <= oy < j + y[k]:
                                silicon.append(solution[ox][oy][k])
                            else:
                                silicon.append(Not(solution[ox][oy][k]))
                    possible_sols.append(And(silicon))
            s.add(exactly_one(possible_sols))

        # puts the silicon with larger area in the bottom left corner
        solver.add([And(solution[0][0][biggest_silicon])])

        if solver.check() == sat:
            time = timer() - start
            print("model solved with length:", l, "in time: ", time, "s")
            solved = True
            print(time)
        else:
            print("Failed to solve with length: ", l)
            l = l + 1
            

    get_solution(solver.model(), solution, w, l, n, maxlen)
    
    return solver.model(), l



def main():
    input_directory = "./instances/ins-4.txt"
    #output_directory = ".\instances\ins-11.txt" #to define when write file
    solve_problem(input_directory)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

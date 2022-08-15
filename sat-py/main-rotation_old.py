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

        # puts the silicon with larger area in the bottom left corner
        solver.add([And(solution[0][0][biggest_silicon])])

        #if square chips do not rotate
        for k in range(n):
            if x[k] == y[k]:
                solver.add([Not(rotation[k])])

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
            #solver.add(exactly_one(possible_sols))

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

            solver.add(exactly_one([non_rotated_silicons, rotated_silicons]))

        if solver.check() == sat:
            time = timer() - start
            print("model solved with length:", l, "in time: ", time, "s")
            #print(solver.model())
            solved = True
            for k in range(n):
                print(z3.is_false(rotation[k]))
        else:
            print("Failed to solve with length : ", l)
            l = l + 1
            #condition to stop

    p_x_sol, p_y_sol, rot_sol, l = get_solution(solver.model(), solution, w, l, n, maxlen, rotation)

    #size_l = np.max(p_y_sol)
    #print("print  p_y_sol_size_l", size_l)
    output_matrix = display_solution(p_x_sol, p_y_sol, w, n, x, y, l, rot_sol)

    #PLOT SOLUTION
    fig, ax = plt.subplots(figsize=(5, 5))
    sns.heatmap(output_matrix,cmap="BuPu", linewidths=.5, linecolor="black", ax=ax)
    #sns.color_palette("Set2")
    plt.show()
    #cmap="BuPu"
    #"PiYG"
    return solver.model(), l


def main():
    input_directory = "./instances/ins-4.txt"
    # output_directory = ".\instances\ins-11.txt" #to define when write file
    solve_problem(input_directory)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


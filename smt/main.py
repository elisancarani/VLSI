from os.path import *
from z3 import *
from timeit import default_timer as timer
from utils import *

def solve_problem(input_directory):

    w, n, x, y, maxlen = read_file(input_directory)

    sol_x = [Int(f"sol_x{i}") for i in range(n)]
    sol_y = [Int(f"sol_y{i}") for i in range(n)]
    l = Int("l")

    sum = 0
    for k in range(n):
        sum += x[k] * y[k]
    minlen = math.floor(sum / w)

    biggest_silicon = 0
    for k in range(n):
        if x[biggest_silicon] * y[biggest_silicon] < x[k] * y[k]:
            biggest_silicon = k

    optimizer = Optimize()

    optimizer.set("timeout", 100000)

    optimizer.add(And(minlen <= l, l <= maxlen))

    #making sure the silicons don't spill out of the box
    for k in range(n):
        optimizer.add(And(sol_x[k] >= 0,
                          sol_y[k] >= 0,
                          sol_x[k] <= w-x[k],
                          sol_y[k] <= l-y[k]))

    for k1 in range(n):
        for k2 in range(n):
            if k1 != k2:
                #no solutions can be the same
                optimizer.add(Not(And(sol_x[k1] == sol_x[k2], sol_y[k1] == sol_y[k2])))
                #no overlap
                optimizer.add(Or(sol_x[k1] >= sol_x[k2] + x[k2],
                                 sol_x[k1] <= sol_x[k2] - x[k1],
                                 sol_y[k1] >= sol_y[k2] + y[k2],
                                 sol_y[k1] <= sol_y[k2] - y[k1]))

    #CUMULATIVE X
    # REF: https://glossary.informs.org/ver2/mpgwiki/index.php?title=Cumulative_constraint
    for i in range(w):
        l_sum = 0
        for k in range(n):
            l_sum += If(And(sol_x[k] <= i, i < sol_x[k] + x[k]), y[k], 0)
        optimizer.add(l >= l_sum)

    # CUMULATIVE Y slows down
    """for i in range(maxlen):
       w_sum = 0
       for k in range(n):
           w_sum += If(And(sol_y[k] <= i, i < sol_y[k] + y[k]), x[k], 0)
       optimizer.add(w >= w_sum)"""

    optimizer.add(And(sol_x[biggest_silicon] == 0, sol_y[biggest_silicon] == 0))

    #Symmetry breaking
    for k1 in range(n):
        for k2 in range(n):
            if k1 < k2 and x[k1] == x[k2] and y[k1] == y[k2]:
                optimizer.add(Or(sol_x[k1] < sol_x[k2], And(sol_x[k1] == sol_x[k2], sol_y[k1] <= sol_y[k2])))

    optimizer.minimize(l)

    start = timer()
    if optimizer.check() == sat:
        time = timer() - start
        print("total time: ", time)
        model = optimizer.model()
        final_x, final_y, final_l, final_r = get_solution(model, sol_x, sol_y, l, n)

        print("length: ", final_l)
        print(final_x, final_y)
        print(final_r)

        '''output_matrix = display_solution(final_x, final_y, w, n, x, y, final_l, final_r)

            # PLOT SOLUTION
            fig, ax = plt.subplots(figsize=(5, 5))
            sns.heatmap(output_matrix, cmap="BuPu", linewidths=.5, linecolor="black", ax=ax)
            # sns.color_palette("Set2")
            plt.show()'''

        return final_x, final_y, w, n, x, y, final_l, final_r, time
    else:
        print("solution not found in time")
        return None


def main():
    #input_directory = "./instances/ins-18.txt"
    #final_x, final_y, w, n, x, y, final_l, final_r = solve_problem(input_directory)
    solve_all(solve_problem, "./out/noRotation")




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


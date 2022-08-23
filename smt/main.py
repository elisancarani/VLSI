from z3 import *
from timeit import default_timer as timer
from utils import *

def solve_problem(input_directory):

    w, n, x, y, maxlen = read_file(input_directory)

    sol_x = [Int(f"sol_x{i}") for i in range(n)]
    sol_y = [Int(f"sol_y{i}") for i in range(n)]
    l = Int("l")

    optimizer = Optimize()


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

    output_matrix = display_solution(final_x, final_y, w, n, x, y, final_l, final_r)

    # PLOT SOLUTION
    fig, ax = plt.subplots(figsize=(5, 5))
    sns.heatmap(output_matrix, cmap="BuPu", linewidths=.5, linecolor="black", ax=ax)
    # sns.color_palette("Set2")
    plt.show()
    return optimizer.model(), l

    #TODO
    #symmetry breaking and cumulative


def main():
    input_directory = "./instances/ins-15.txt"
    #output_directory = ".\instances\ins-11.txt" #to define when write file
    solve_problem(input_directory)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

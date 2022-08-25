from z3 import *
from timeit import default_timer as timer
from utils import *

def solve_problem(input_directory):

    w, n, x_before, y_before, maxlen = read_file(input_directory)

    sol_x = [Int(f"sol_x{i}") for i in range(n)]
    sol_y = [Int(f"sol_y{i}") for i in range(n)]
    rotation = [Bool(f"r{i}") for i in range(n)]
    l = Int("l")

    x = [Int(f"x{i}") for i in range(n)]
    y = [Int(f"y{i}") for i in range(n)]

    sum = 0
    for k in range(n):
        sum += x_before[k] * y_before[k]
    minlen = math.floor(sum / w)

    biggest_silicon = 0
    for k in range(n):
        if x_before[biggest_silicon] * y_before[biggest_silicon] < x_before[k] * y_before[k]:
            biggest_silicon = k

    optimizer = Optimize()

    optimizer.add(And(minlen <= l, l <= maxlen))

    for k in range(n):
        optimizer.add(Or(And(And(x[k] == x_before[k], y[k] == y_before[k]), Not(rotation[k])), And(And(x[k] == y_before[k], y[k] == x_before[k]), rotation[k])))
        if x_before[k] == y_before[k]:
            optimizer.add(Not(rotation[k]))

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
        final_x, final_y, final_l, final_r = get_solution(model, sol_x, sol_y, l, n, rotation)
        final_dim_x, final_dim_y = get_dimentions(model, x, y, n, final_r)

        print("length: ", final_l)
        print(final_x, final_y)
        print(final_dim_x)
        print(final_r)

    output_matrix = display_solution(final_x, final_y, w, n, x_before, y_before, final_l, final_r)

    # PLOT SOLUTION
    fig, ax = plt.subplots(figsize=(5, 5))
    sns.heatmap(output_matrix, cmap="BuPu", linewidths=.5, linecolor="black", ax=ax)
    # sns.color_palette("Set2")
    plt.show()
    return optimizer.model(), l

def main():
    input_directory = "./instances/ins-2.txt"
    #output_directory = ".\instances\ins-11.txt" #to define when write file
    solve_problem(input_directory)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


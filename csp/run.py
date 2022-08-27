import os
from datetime import timedelta
from os.path import exists
from minizinc import Model, Solver, Instance, Status
from timeit import default_timer as timer


def read_file(in_file):
    f = open(in_file, "r")
    lines = f.read().splitlines()

    w = int(lines[0])
    n = int(lines[1])

    x = []
    y = []
    for i in range(int(n)):
        split = lines[i + 2].split(' ')
        x.append(int(split[0]))
        y.append(int(split[1]))

    maxlen = sum(y)

    return w, n, x, y, maxlen


def write_file(file, final_x, final_y, w, n, x, y, l, r, time):
    f = open(file, 'w')
    f.write(f"n, w: {n} {w}\n")
    f.write(f"[")
    for k in range(n):
        if k == n-1:
            f.write(f"{x[k]}")
        else:
            f.write(f"{x[k]}, ")
    f.write(f"]\t")
    f.write(f"[")
    for k in range(n):
        if k == n - 1:
            f.write(f"{y[k]}")
        else:
            f.write(f"{y[k]}, ")
    f.write(f"]\n")

    f.write(f"solution: {l}\n")

    f.write(f"[")
    for k in range(n):
        if k == n - 1:
            f.write(f"{final_x[k]}")
        else:
            f.write(f"{final_x[k]}, ")
    f.write(f"]\t")
    f.write(f"[")
    for k in range(n):
        if k == n - 1:
            f.write(f"{final_y[k]}")
        else:
            f.write(f"{final_y[k]}, ")
    f.write(f"]\n")
    f.write(f"[")
    for k in range(n):
        if k == n - 1:
            f.write(f"{r[k]}")
        else:
            f.write(f"{r[k]}, ")
    f.write(f"]")

    f.write(f"\ntime: {time}\n")

    return

def solve_all(rotation):
    if rotation == False:
        model_name = "./csp.mzn"
        out_dir = "./out/noRotation"
    else:
        model_name = "./csp-rotation.mzn"
        out_dir = "./out/Rotation"
    input_dir = "./instances"
    '''plot_dir = os.path.join("./plots")
    if not exists(plot_dir):
        os.makedirs(plot_dir)'''
    if not exists(out_dir):
        os.makedirs(out_dir)

    for file in sorted(os.listdir(input_dir)):
        name = file.split(os.sep)[-1].split('.')[0]
        out_name = name.lower().replace("ins", "out").replace('.dzn', '.txt')

        # instance = read_file(os.path.join(input_dir, file))
        print(f"Solving instance {name}")

        w, n, x, y, maxlen = read_file(os.path.join(input_dir, file))
        silicons = []
        for i in range(n):
            silicons.append(x[i])
            silicons.append(y[i])

        model = Model(model_name)
        solver = Solver.lookup("gecode")

        inst = Instance(solver, model)
        inst["w"] = w
        inst["n"] = n
        inst["silicons"] = silicons


        start_time = timer()
        result = inst.solve(timeout=timedelta(seconds=300), free_search=True)
        time = timer() - start_time

        if result.status is Status.OPTIMAL_SOLUTION:
            final_sol = result.solution.solution
            l = result.solution.l
            if rotation:
                r = result.solution.rotation
            else:
                r = []
                for k in range(n):
                    r.append("False")

            final_x = []
            final_y = []
            for k in range(n):
                final_x.append(final_sol[k][0])
                final_y.append(final_sol[k][1])

            print(final_x, final_y, w, n, x, y, l, r, time)

            write_file(os.path.join(out_dir, out_name + ".txt"), final_x, final_y, w, n, x, y, l, r, time)
        else:
            print("not found")
        '''if sol is not None:
            write_file(os.path.join(out_dir, out_name + ".txt"), sol[0], sol[1], sol[2], sol[3], sol[4], sol[5],
                       sol[6],
                       sol[7], sol[8])
            print("Solution to instance ", file, "found in time", sol[8])
        else:
            print("Solution not found in time")'''


def main():
    #input_directory = "./instances/ins-1.txt"
    #output_directory = ".\instances\ins-11.txt" #to define when write file
    #solve_problem(input_directory)
    rotation = True
    solve_all(rotation)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
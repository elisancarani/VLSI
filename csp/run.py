import os
from os.path import exists

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
        model = "./csp"
        out_dir = "./out/noRotation"
    else:
        model = "./cps-rotation"
        out_dir = "./out/Rotation"
    input_dir = "./instances/instancesdzn"
    '''plot_dir = os.path.join("./plots")
    if not exists(plot_dir):
        os.makedirs(plot_dir)'''
    if not exists(out_dir):
        os.makedirs(out_dir)

    input_files = ["ins-1.dzn", "ins-2.dzn", "ins-10.dzn"]

    for file in input_files:
        name = file.split(os.sep)[-1].split('.')[0]
        out_name = name.lower().replace("ins", "out")

        # instance = read_file(os.path.join(input_dir, file))
        print(f"Solving instance {name}")

        os.system(f"minizinc --solver Chuffed -f --solver-time-limit 500000 --all-solutions --output-time {model} {os.path.join(input_dir, file)} --output-to-file {out_dir}")
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
    rotation = False
    solve_all(rotation)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
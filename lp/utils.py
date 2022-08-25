import os
from os.path import exists

import numpy as np

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
    f.write(f"input data: {n} {w}\n")
    f.write(f"[")
    for k in range(n):
        f.write(f"{x[k]} ")
    f.write(f"]\t")
    f.write(f"[")
    for k in range(n):
        f.write(f"{y[k]} ")
    f.write(f"]\n")

    f.write(f"solution: {l}\n")

    f.write(f"[")
    for k in range(n):
        f.write(f"{final_x[k]} ")
    f.write(f"]\t")
    f.write(f"[")
    for k in range(n):
        f.write(f"{final_y[k]} ")
    f.write(f"]\n")
    f.write(f"[")
    for k in range(n):
        f.write(f"{r[k] }")
    f.write(f"]")

    f.write(f"\ntime: {time}\n")

    return


def display_solution(p_x_sol, p_y_sol, w, n, x, y, l, rotation):

    final_solution = np.empty(len(p_x_sol)*2, dtype=object)

    silicons = np.empty(len(x)*2, dtype=object)
    print("silicons", silicons)

    #max_height = np.max(y)

    k=0
    elem1 = 0
    for i in p_x_sol:
        final_solution[k] = i
        final_solution[k+1] = p_y_sol[elem1]
        elem1 +=1
        k=k+2
    print("final solution", final_solution)

    '''q=0
    elem = 0
    for i in x:
        silicons[q] = i
        silicons[q+1] = y[elem]
        elem += 1
        q=q+2
    print("riempito s", silicons)'''

    q=0
    for i in range(n):
        if rotation[i] == True:
            silicons[q] = y[i]
            silicons[q+1] = x[i]
        else:
            silicons[q] = x[i]
            silicons[q+1] = y[i]
        q = q+2

    #print("N", n)
    #print("Y", y)
    #print("l", l)
    #print("max height", max_height)
    #la matrice è alta come la posizione più alta delle y + l'altezza del rettangolo in quella posizione

    #l_f = max_height + l
    #print("l_F", l_f)
    #print("w", w)
    output_matrix = np.zeros((w, l))

    for i in range(n):
        base = silicons[2 * i]
        altezza = silicons[2 * i + 1]
        #print("n:", i)
        #print("base: ", base);
        #print("altezza: ", altezza)
        for j in range(base):
            for q in range(altezza):
                output_matrix[final_solution[2 * i] + j, final_solution[2 * i + 1] + q] = i + 1
                #print(i,j,q)
    print(output_matrix)

    return output_matrix

def get_solution(sol_x, sol_y, n, rotation=None):
    x = []
    y = []
    r = []
    for k in range(n):
        x.append(round(sol_x[k].varValue))
        y.append(round(sol_y[k].varValue))
        if rotation is not None:
            r.append(round(rotation[k].varValue))
        else:
            r.append(False)
    #print(x, y)
    return x,y,r

def display_solution(p_x_sol, p_y_sol, w, n, x, y, l, rotation=None):

    final_solution = np.empty(len(p_x_sol)*2, dtype=object)

    silicons = np.empty(len(x)*2, dtype=object)

    k=0
    elem1 = 0
    for i in p_x_sol:
        final_solution[k] = i
        final_solution[k+1] = p_y_sol[elem1]
        elem1 +=1
        k=k+2
    #print("final solution", final_solution)

    q=0
    for i in range(n):
        if rotation[i] == True:
            silicons[q] = y[i]
            silicons[q+1] = x[i]
        else:
            silicons[q] = x[i]
            silicons[q+1] = y[i]
        q = q+2

    output_matrix = np.zeros((w, l))

    for i in range(n):
        base = silicons[2 * i]
        altezza = silicons[2 * i + 1]

        for j in range(base):
            for q in range(altezza):
                output_matrix[final_solution[2 * i] + j, final_solution[2 * i + 1] + q] = i + 1
    print("rotation: ", rotation)
    print(output_matrix)

    return output_matrix

def solve_all(solve_problem, out_dir):
    input_dir = "./instances"
    '''plot_dir = os.path.join("./plots")
    if not exists(plot_dir):
        os.makedirs(plot_dir)'''
    if not exists(out_dir):
        os.makedirs(out_dir)

    for file in sorted(os.listdir(input_dir)):
        name = file.split(os.sep)[-1].split('.')[0]
        out_name = name.lower().replace("ins", "out")

        # instance = read_file(os.path.join(input_dir, file))
        print(f"Solving instance {name}")

        sol = solve_problem(os.path.join(input_dir, file))
        if sol is not None:
            '''plot_file = os.path.join(plot_dir, out_name + '.png')
            output_matrix = display_solution(final_x, final_y, w, n, x, y, l, r)
            # PLOT SOLUTION
            #fig, ax = plt.subplots(figsize=(5, 5))
            fig = go.Figure()
            sns.heatmap(output_matrix, cmap="BuPu", linewidths=.5, linecolor="black", ax=ax)
            # sns.color_palette("Set2")
            #plt.show()
            fig.write_image(plot_file, width=1200, height=1200)'''

            write_file(os.path.join(out_dir, out_name + ".txt"), sol[0], sol[1], sol[2], sol[3], sol[4], sol[5],
                       sol[6],
                       sol[7], sol[8])
            print("Solution to instance ", file, "found in time", sol[8])
        else:
            print("Solution not found in time")
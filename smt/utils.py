from os.path import exists
import numpy as np
import random
from itertools import combinations
from z3 import *
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display, HTML


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

def get_solution(model, sol_x, sol_y, l, n, rotation=None):
    x = []
    y = []
    r = []
    for k in range(n):
        x.append(model[sol_x[k]].as_long())
        y.append(model[sol_y[k]].as_long())
        if rotation is not None:
            r.append(model[rotation[k]])
        else:
            r.append(False)
    l = model[l].as_long()
    #print(x, y)
    return x,y,l,r

'''def get_dimensions(model, dimx, dimy, n, rotation):
    x = []
    y = []
    for k in range(n):
        if rotation[k] == False:
            x.append(model[dimx[k]].as_long())
            y.append(model[dimy[k]].as_long())
        else:
            x.append(model[dimy[k]].as_long())
            y.append(model[dimx[k]].as_long())
    return x,y'''


def display_solution(p_x_sol, p_y_sol, w, n, x, y, l, rotation):
    final_solution = np.empty(len(p_x_sol) * 2, dtype=object)

    silicons = np.empty(len(x) * 2, dtype=object)

    k = 0
    elem1 = 0
    for i in p_x_sol:
        final_solution[k] = i
        final_solution[k + 1] = p_y_sol[elem1]
        elem1 += 1
        k = k + 2
    print("final solution", final_solution)

    q = 0
    for i in range(n):
        if rotation[i] == True:
            silicons[q] = y[i]
            silicons[q + 1] = x[i]
        else:
            silicons[q] = x[i]
            silicons[q + 1] = y[i]
        q = q + 2

    output_matrix = np.zeros((w, l))

    for i in range(n):
        base = silicons[2 * i]
        altezza = silicons[2 * i + 1]
        for j in range(base):
            for q in range(altezza):
                output_matrix[final_solution[2 * i] + j, final_solution[2 * i + 1] + q] = i + 1
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


"""
def display_nqueens(sol):
    board = [[0] * len(sol) for i in range(len(sol))]
    for x, y in sol:
        board[x][y] = 1
    for i in range(len(board)):
        for j in range(len(board[0])):
            symbol = '♛' if board[i][j] == 1 else '.'
            print(symbol, end=' ')
        print()

def display_pigeons(sol, m):
    board = [0]*m
    for y in sol:
        board[y] = 1
    for i in range(len(board)):
        symbol = '[🕊]' if board[i] == 1 else '[.]'
        print(symbol, end=' ')
    print()

def display_color_graph(E, sol = None):
    G = nx.Graph()
    G.add_edges_from(E)
    colors = {}
    if sol:
        for v, c in sol:
            colors[c] = colors.get(c, random.random())
        assigned_colors = {v:colors[c] for v, c in sol}
        node_colors = [assigned_colors.get(node, 0.25) for node in G.nodes()]
    else:
        node_colors = [0] * len(list(set([v1 for v1, _ in E] + [v2 for _, v2 in E])))
    nx.draw(G, with_labels = True, node_color=node_colors, font_color='white') 

def display_nurses_shifts(sol, num_nurses, num_shifts, num_days):
    for d in range(num_days):
        print('Day %i' % d)
        for n in range(num_nurses):
            is_working = False
            for s in range(num_shifts):
                if (n, d, s) in sol:
                    is_working = True
                    print('  Nurse %i works shift %i' % (n, s))
            if not is_working:
                print('  Nurse {} does not work'.format(n))

def display_sudoku(sol):
    fig, ax = plt.subplots(figsize=(4, 4))
    for l in range(9):
        for c in range(9):
            v = sol[c][l]
            s = " "
            if v > 0:
                s = str(v)
            ax.text(l+0.5, 8.5-c, s, va='center', ha='center')
        ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_xticks(np.arange(9))
    ax.set_yticks(np.arange(9))
    ax.grid()
    plt.show()


def display_scheduling(sol):
    schedule = pd.DataFrame(sol)

    jobs = sorted(list(schedule['job'].unique()))
    machines = sorted(list(schedule['machine'].unique()))
    makespan = schedule['finish'].max()

    bar_style = {'alpha': 1.0, 'lw': 25, 'solid_capstyle': 'butt'}
    text_style = {'color': 'white', 'weight': 'bold', 'ha': 'center', 'va': 'center'}
    colors = mpl.cm.Dark2.colors

    fig, ax = plt.subplots(figsize=(8, len(machines) + 1))

    for _, row in schedule.iterrows():
        m = row['machine']
        j = row['job']
        xs = row['start']
        xf = row['finish']
        ax.plot([xs, xf], [m + 1] * 2, c=colors[j % 8], **bar_style)
        ax.text((xs + xf) / 2, m + 1, j, **text_style)

    ax.set_title('Machine Schedule')
    ax.set_ylabel('Machine')
    ax.set_xlabel('Time')

    for _, s in enumerate([jobs, machines]):
        ax.set_ylim(0.5, len(s) + 0.5)
        ax.set_yticks(range(1, 1 + len(s)))
        ax.set_yticklabels(s)

    ax.text(makespan, ax.get_ylim()[0] - 0.2, "{0:0.1f}".format(makespan), ha='center', va='top')
    ax.plot([makespan] * 2, ax.get_ylim(), 'r--')
    ax.grid(True)

    fig.tight_layout()
    plt.show()"""

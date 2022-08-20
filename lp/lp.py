import math
import seaborn as sns
import matplotlib.pyplot as plt
from pulp import *
from utils import *

def solve_problem(input_directory):
    path_to_cplex = r"C:\Program Files\IBM\ILOG\CPLEX_Studio221\cplex\bin\x64_win64\cplex.exe"
    w, n, x, y, maxlen = read_file(input_directory)

    biggest_silicon = 0
    for k in range(n):
        if x[biggest_silicon] * y[biggest_silicon] < x[k] * y[k]:
            biggest_silicon = k

    sum = 0
    for k in range(n):
        sum += x[k] * y[k]
    minlen = math.floor(sum / w)

    l = LpVariable("l", lowBound=minlen, upBound=maxlen, cat=LpInteger)

    sol_x = [LpVariable(f"sol_x{i+ 1:02d}", lowBound=0, upBound=w, cat=LpInteger) for i in range(n)]
    sol_y = [LpVariable(f"sol_y{j}", lowBound=0, upBound=maxlen, cat=LpInteger) for j in range(n)]

    place_x1 = [[LpVariable(f"place_x1{i+ 1:02d}{j+ 1:02d}", cat=LpBinary) for i in range(n)] for j in range(n)]
    place_x2 = [[LpVariable(f"place_x2{i+ 1:02d}{j+ 1:02d}", cat=LpBinary) for i in range(n)] for j in range(n)]
    place_y1 = [[LpVariable(f"place_y1{i+ 1:02d}{j+ 1:02d}", cat=LpBinary) for i in range(n)] for j in range(n)]
    place_y2 = [[LpVariable(f"place_y2{i+ 1:02d}{j+ 1:02d}", cat=LpBinary) for i in range(n)] for j in range(n)]

    problem = LpProblem("StripPacking", LpMinimize)

    problem += l, 'objective function'

    for k in range(n):
        problem += sol_x[k] <= w-x[k]
        problem += sol_y[k] <= l-y[k]

    for k1 in range(n):
        for k2 in range(n):
            if k1 != k2:
                problem += sol_x[k1] >= sol_x[k2] + x[k2] - w*place_x1[k1][k2] #if x is 0 then it's true
                problem += sol_x[k1] <= sol_x[k2] - x[k1] + w*place_x2[k1][k2]
                problem += sol_y[k1] >= sol_y[k2] + y[k2] - maxlen*place_y1[k1][k2]
                problem += sol_y[k1] <= sol_y[k2] - y[k1] + maxlen*place_y2[k1][k2]
                problem += 2 <= place_x1[k1][k2] + place_x2[k1][k2] + place_y1[k1][k2] + place_y2[k1][k2] <= 3

    problem += sol_y[biggest_silicon] == 0
    problem += sol_x[biggest_silicon] == 0

    solver = CPLEX_CMD(path=path_to_cplex)

    problem.solve(solver)

    print(l.varValue)
    for k in range(n):
        print(sol_x[k].varValue)
        print(sol_y[k].varValue)

    '''final_sol_x = []
    final_sol_y = []
    #print(l.varValue)
    for k in range(n):
        final_sol_x.append(sol_x[k].varValue)
        final_sol_y.append(sol_y[k].varValue)

    print(final_sol_x, final_sol_y)

    output_matrix = display_solution(final_sol_x, final_sol_y, w, n, x, y, l)

    # PLOT SOLUTION
    fig, ax = plt.subplots(figsize=(5, 5))
    sns.heatmap(output_matrix, cmap="BuPu", linewidths=.5, linecolor="black", ax=ax)
    # sns.color_palette("Set2")
    plt.show()'''

#TODO
#ADD TIMER AND GETSOLUTION AND ROTATION

def main():
    input_directory = "./instances/ins-9.txt"
    #output_directory = ".\instances\ins-11.txt" #to define when write file
    solve_problem(input_directory)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
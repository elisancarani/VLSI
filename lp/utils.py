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
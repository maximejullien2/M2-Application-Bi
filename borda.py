import re
import numpy as np
import pandas as pd
import networkx as nx 
import matplotlib.pyplot as plt
import promethee


def display(decompte_borda):
    """
    Create a png file to show result of borda algorithm.

    Args:
        decompte_borda (array): Reprensent result of borda algorithm.

    """
    plt.clf()
    g = nx.DiGraph()
    arg_array = promethee.sort(decompte_borda, -1)
    print(arg_array)
    i = 0
    ancien = "C"+str(arg_array[i])
    for j in range(i,len(arg_array) - 1):
            if decompte_borda[arg_array[j]]==decompte_borda[arg_array[j+1]]:
                ancien += ",C"+str(arg_array[j+1])
                i=i+1
            else:
                break
    while (i < len(arg_array)-1):
        message = "C"+str(arg_array[i+1])
        for j in range(i+1,len(arg_array) - 1):
            if decompte_borda[arg_array[j]]==decompte_borda[arg_array[j+1]]:
                message += ",C"+str(arg_array[j+1])
                i=i+1
            else:
                break
        g.add_edge(ancien,message)
        ancien = message
        i += 1
    nx.draw(g, with_labels = True)
    plt.savefig("borda.png")


def get_doublon(borda_point, j, i, value, array, arg_array):
    """
    Iterate when we get doublon.

    Args:
        borda_point (array): Array we treat.
        j (int): Position we start to treat.
        i (int): Position we need to change.
        value (int): To know where we are for the value.
        array (array): Array of value .
        arg_array (array): Array represent agument sorted.

    Returns:
        Bool : Reprensent if detect doublon or not .
    """
    nb_doublou = 2
    position_to_treat = [arg_array[j], arg_array[j+1]]
    j = j+1
    while j < len(arg_array):
        if j < len(arg_array)-1 and array[arg_array[j]] == array[arg_array[j+1]]:
            position_to_treat.append(arg_array[j+1])
            nb_doublou += 1
            j += 1
        else:
            break
    for y in position_to_treat:
        borda_point[i][y] = value + 1/nb_doublou
    value += (nb_doublou-1)
    return borda_point, value, j

def detect_doublon(j, array, arg_array):
    """
    Detect if their is a doublon for next iteration.

    Args:
        j (int): Position where we are.
        array (array): Array of value .
        arg_array (array): Array represent agument sorted.

    Returns:
        Bool : Reprensent if detect doublon or not .
    """
    if j < len(arg_array)-1 and array[arg_array[j]] == array[arg_array[j+1]]:
        return True 
    return False

def borda(data , array_operation_type):
    """
    Launch a borda algorithm.

    Args:
        data (Panda array): Represente data we want to treat.
        array_type_operation (array): Represente action we want to do on each critère ("min" ou "max").

    Returns:
        Array_list : Return value for each action (A).
    """
    columns_name = []
    for i in data.columns:
        if re.search("^C[0-9]+",i):
            columns_name.append(i)

    borda_point = np.zeros((len(data.index), len(columns_name)))
    decompte_borda = np.zeros(len(columns_name))

    for i in range(len(data.index)):
        array = []
        for j in range(len(columns_name)):
            array.append(data[columns_name[j]][i])
        if array_operation_type[i] == "max":
            arg_array = promethee.sort(array, 0)
        else:
            arg_array = promethee.sort(array, -1)
        value = 1
        j = 0
        while j < len(arg_array):
            if detect_doublon(j, array, arg_array):
                borda_point, value, j = get_doublon(borda_point, j, i, value, array, arg_array)
            else:
                borda_point[i][arg_array[j]] = value
            value +=1
            j+=1

    for x in range(len(borda_point[0])):
        for y in range(len(borda_point)):
            decompte_borda[x] += borda_point[y][x]
    return decompte_borda

if __name__ == "__main__":
    data = pd.read_csv('data/donneesFusionerDecher.csv')
    min = []
    for i in range(0,data.index.size):
        min.append("min")
    print(borda(data,min))
    display(borda(data,min))

    data = pd.read_csv('data/donneesVoiture.csv')
    operation = ["min", "max", "min", "min", "max", "max", "min"]
    print(borda(data,operation))
    display(borda(data,operation))
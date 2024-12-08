import re
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def display_result(type, result_promethee):
    """
    Show result of Prométhée algorithm.
    Args:
        type (int =1 or 2): Represent the type of Promethee we want to display.
        result_promethee (Array or Array[Array[]]): Array who represent prométhée result.

    """
    print("Voici les résultast de Prométhée",end="")
    if type == 1:
        print("I:")
        print("Φ^+ = ","C"+str(result_promethee[0][0]+1),end="")
        for i in range (1,len(result_promethee[0])):
            if result_promethee[0][i] != result_promethee[0][i-1]:
                print(" > C"+str(result_promethee[0][i]+1),end="")
            else:
                print(" = C"+str(result_promethee[0][i]+1),end="")

        print()
        print("Φ^- = ","C"+str(result_promethee[1][0]+1),end="")
        for i in range (1,len(result_promethee[1])):
            if result_promethee[1][i] != result_promethee[1][i-1]:
                print(" > C"+str(result_promethee[1][i]+1),end="")
            else:
                print(" = C"+str(result_promethee[1][i]+1),end="")
        print()
    elif type == 2:
        print("II:")
        print("Φ = ","C"+str(result_promethee[0]+1),end="")
        for i in range (1,len(result_promethee)):
            if result_promethee[i] != result_promethee[i-1]:
                print(" > C"+str(result_promethee[i]+1),end="")
            else:
                print(" = C"+str(result_promethee[i]+1),end="")
        print("")
    else:
        exit("Erreur le type de Prométhée donnée est différent de 1 ou 2")

def create_graphe_type1_lien_identique(result_promethee, visiter, g):
    """
    Create edge between point if only the edge is in two phi ( positif and negatif)
    Args:
        result_promethee (Array or Array[Array[]]): Array who represent prométhée result.
        visiter (Array): Array who represent if a point have already create a edge.
        g (nx.Digraph): Represent the graph we try to create.

    Returns:
        visiter , g : Represent work we done on this graph.
            """
    for i in range(0,len(result_promethee[0])-1):
        if result_promethee[0][i] == result_promethee[1][i] and result_promethee[0][i+1] == result_promethee[1][i+1]:
            g.add_edge("C"+str(result_promethee[0][i]+1), "C"+str(result_promethee[0][i+1]+1))
            visiter[result_promethee[0][i]] = 0
    for i in range(0,len(result_promethee[0])-1):
        for j in range(0, len(result_promethee[1]) - 1):
            if result_promethee[0][i] == result_promethee[1][j] and i!=(len(result_promethee[0]) - 1) and j != (len(result_promethee[1]) - 1):
                if result_promethee[0][i+1] == result_promethee[1][j+1]:
                    g.add_edge("C"+str(result_promethee[0][i]+1), "C"+str(result_promethee[0][i+1]+1))
                    visiter[result_promethee[0][i]] = 0
    return visiter, g

def create_graphe_type1_lien_non_identique(result_promethee, visiter, g):
    """
    Create edge between point if the edge is not directly link in two phi ( positif and negatif)
    Args:
        result_promethee (Array or Array[Array[]]): Array who represent prométhée result.
        visiter (Array): Array who represent if a point have already create a edge.
        g (nx.Digraph): Represent the graph we try to create.

    Returns:
        visiter , g : Represent work we done on this graph.
            """
    array_superieur = []
    #Will compare each point for each phi.
    #If a point is better of another, I will have 0 to his position.
    #Else he will have 1, signify he is better than this point
    for i in range(0,len(result_promethee[0])):
        phi_neg = np.ones(len(result_promethee[1]))
        phi_positivie = np.ones(len(result_promethee[0]))
        position_positif = np.argwhere(result_promethee[0] == i)
        position_neg = np.argwhere(result_promethee[1] == i)
        for j in range(0,len(result_promethee[0])):
            if np.argwhere(result_promethee[0] == j) <= position_positif:
                phi_positivie[j] = 0
            if np.argwhere(result_promethee[1] == j) <= position_neg:
                phi_neg[j] = 0
        array_superieur.append([phi_positivie, phi_neg])

    
    #He will add new edge if he already didn't have a edge.
    #In this case he will create a edge with best worst result if he is better with two phi.
    for i in range(0,len(result_promethee[0])-1):
        if visiter[result_promethee[0][i]] == 1:
            j = i+1
            while j < len(result_promethee[0]):
                if array_superieur[result_promethee[0][i]][0][result_promethee[0][j]] == 1 and array_superieur[result_promethee[0][i]][1][result_promethee[0][j]] == 1:
                    g.add_edge("C"+str(result_promethee[0][i]+1), "C"+str(result_promethee[0][j]+1))
                    break
                else:
                    j +=1
        if visiter[result_promethee[1][i]] == 1:
            j = i+1
            while j < len(result_promethee[1]):
                if array_superieur[result_promethee[1][i]][0][result_promethee[1][j]] == 1 and array_superieur[result_promethee[1][i]][1][result_promethee[1][j]] == 1:
                    g.add_edge("C"+str(result_promethee[1][i]+1), "C"+str(result_promethee[1][j]+1))
                    break
                else:
                    j +=1
    return visiter, g

def create_graph(type, result_promethee, filename):
    """
    Function to create a graph who will display result of prométhée algorithm in a filename.
    Args:
        type (int =1 or 2) : Represent the type of Promethee we used.
        result_promethee (Array or Array[Array[]]): Array who represent prométhée result.
        filename (string): Name of output file.:
    """
    plt.clf()
    g = nx.DiGraph()
    if type == 2:
        for i in range(0,len(result_promethee)-1):
            g.add_edge("C"+str(result_promethee[i]+1), "C"+str(result_promethee[i+1]+1))
        nx.draw(g, with_labels=True)
        plt.savefig(filename + ".png")
    else:
        visiter = np.ones(len(result_promethee[0]))
        visiter, g = create_graphe_type1_lien_identique(result_promethee, visiter, g)
        visiter, g = create_graphe_type1_lien_non_identique(result_promethee, visiter, g)
        nx.draw(g, with_labels=True)
        plt.savefig(filename + ".png")

def comparaison(value_x, value_y, weight,operation, seuil_preference = None):
    """
    Compare two value.

    Args:
        value_x (int): Represent value for an instance x on a specific critere.
        value_y (int): Represent value for an instance y on a specific critere.
        weight (int): Represente weight for a specific critere.
        operation (string = "max" or = "min"): Represente operation we want to treat.
        seuil_preference (int or None): Represente seuil for a categories.

    Returns:
        int : Return weight if operation is true or 0 if false. 
    """
    threshold = seuil_preference
    if threshold == None:
        threshold = 0
    if (operation == "min" and value_x < value_y) or (operation == "max" and value_x > value_y):
        if np.abs(value_x - value_y) >= threshold:
            return weight
        return (np.abs(value_x - value_y) / threshold) * weight
    return 0

def sort(array, type = 0):
    """
    Sort index of an array.

    Args:
        array (Numpy Array): Array we need to sort.
        type (int =-1 or 0): Reprensent if we inverse the sort or not .

    Returns:
        Array : Return an index of array sorted.
    """
    if type == -1: 
        empty = []
        array_sort = np.argsort(array)
        i = 0
        while i < len(array_sort):
            if array[array_sort[len(array_sort) - i -1]] == array[array_sort[len(array_sort) - i -2]]:
                if array_sort[len(array_sort) - i -1] > array_sort[len(array_sort) - i -2]:
                    empty.append(array_sort[len(array_sort) - i - 2])
                    empty.append(array_sort[len(array_sort) - i - 1])
                else:
                    empty.append(array_sort[len(array_sort) - i - 1])
                    empty.append(array_sort[len(array_sort) - i - 2])
                i += 1
            else:
                empty.append(array_sort[len(array_sort) - i - 1])
            i += 1
        return np.array(empty)
    return np.argsort(array)
    
def promethee(selection_mode, data, array_type_operation, seuil_preference_array=None):
    """
    Launch a specific Promethee.

    Args:
        selection_mode (int = 1 or = 2): Select Promethee.
        data (Panda array): Represente data we want to treat.
        array_type_operation (array): Represente action we want to do on each critère ("min" ou "max").
        seuil_preference_array (array or None): Represente seuil for each categories.

    Returns:
        Array_list : Return list of best element for a specific Promethee.

    Raises:
            ValueError: 
                - If selection_mode > 2 ou <= 0.
                - If on indice on array-type_operation is different of "min" and "max".
                - If data is None.
                - if len(array_type_operation) == 0 or array_type_operation == None
    """
    try:
        if selection_mode > 2 or selection_mode <= 0 : 
            raise ValueError("Type of Promethee need to be 1 or 2")
        
        if array_type_operation == None or len(array_type_operation) == 0 :
            raise ValueError("Array array_type_operation is empty or None")

        for i in range(len(array_type_operation)):
            if array_type_operation[i] != "max" and array_type_operation[i] != "min":
                raise ValueError(f"At indice {i} , the array array_type_operation have a data different from 'min' or 'max'.")

        if not pd.notnull(data).all(axis = None): 
            raise ValueError("One value in data is None")
        
    except ValueError as err :
        print(err.args[0])
        exit(0)
    columns_name = []
    for i in data.columns:
        if re.search("^C[0-9]+",i):
            columns_name.append(i)
    table_degres_preference_multicritere = np.zeros((len(columns_name), len(columns_name)))

    phi_negatif = np.zeros(len(columns_name))
    phi_positif = np.zeros(len(columns_name))

    for i in range(len(columns_name)):
        for j in range(len(columns_name)):
            if i != j:
                sum = 0
                for num_line in range(len(data.index)):
                    seuil = None
                    if seuil_preference_array != None:
                        seuil = seuil_preference_array[num_line]
                    sum += comparaison(data[columns_name[i]][num_line],data[columns_name[j]][num_line], data["TrueWeight"][num_line],array_type_operation[num_line], seuil)
                table_degres_preference_multicritere[i][j] = sum
            phi_negatif[j] += table_degres_preference_multicritere[i][j]
            phi_positif[i] += table_degres_preference_multicritere[i][j]
    if selection_mode == 1:
        return [sort(phi_positif,-1) , 
                sort(phi_negatif)]

    return sort(phi_positif - phi_negatif, -1)

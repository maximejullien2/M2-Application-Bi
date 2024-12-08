import re
import pandas as pd
from function import promethee
import networkx as nx
import matplotlib.pyplot as plt

def display_result(weighted_sum_result):
    """
    Function to display the results of the weighted sum algorithm
     Args:
        weighted_sum_result (Array): Array who represent weighted sum result.
    """
    print("Voici le résultat de l'algorithme somme pondérée : ")
    print("C"+str(weighted_sum_result[0]+1),end=" ")
    for i in range(1,len(weighted_sum_result)):
        if weighted_sum_result[i] != weighted_sum_result[i-1]:
            print(" > C"+str(weighted_sum_result[i]+1),end=" ")
        else:
            print(" = C"+str(weighted_sum_result[i]+1),end="")
    print()
    print("Le meilleur candidats est donc : ","C"+str(weighted_sum_result[0]+1))

def create_graph(weighted_sum_result, filename):
    """
    Function to create a graph who will display result of weighted sum algorithm in a filename.
    Args:
        weighted_sum_result (Array): Array who represent weighted sum result.
        filename (string): Name of output file.:
    :return:
    """
    plt.clf()
    g = nx.DiGraph()
    for i in range(len(weighted_sum_result) - 1):
        g.add_edge("C"+str(weighted_sum_result[i]+1),"C"+str(weighted_sum_result[i + 1]+1))
    nx.draw(g, with_labels = True)
    plt.savefig(filename+".png")

def weighted_sum(data,array_type_operation, type_operation):
    """
    Launch a weighted sum on a specific data.

    Args:
        data (Panda array): Represente data we want to treat.
        array_type_operation (array): Represente action we want to do on each critère ("min" ou "max").
        type_operation (array): Represente action we want to do on each critère ("min" ou "max").

    Returns:
        Array_list : Return list order of best element.
    Raises:
            ValueError: 
                - If type_operation is different of "min" and "max".
                - If data is None.
    """
    try:
        if type_operation != "max" and type_operation != "min":
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
    copie = data.loc[:,columns_name[0] : columns_name[len(columns_name) - 1]]
    mean_array = copie.mean(axis = 1)
    std_array = copie.std(axis = 1)
    for i in range(len(mean_array)):
        for j in range(len(columns_name)):
            if std_array[i] == 0:
                data.loc[i, columns_name[j]] = 1
            else:
                data.loc[i, columns_name[j]] = (copie[columns_name[j]][i] - mean_array[i]) / std_array[i]
    result = []
    for i in range(len(columns_name)):
        sum = 0
        for num_line in range(len(data.index)):
            sum += data[columns_name[i]][num_line]*data["TrueWeight"][num_line]
        result.append(sum)
    if type_operation == "max":
        return promethee.sort(result, -1)
    return promethee.sort(result)


if __name__ == '__main__':
    data = pd.read_csv('../data/donneesDecherterie.csv')
    min = []
    for i in range(0,data.index.size):
        min.append("min")
    print(weighted_sum(data,min, "min"))
    display_result(weighted_sum(data,min, "min"))
    create_graph(weighted_sum(data, min, "min"), "weighted_sum_decher")
    data = pd.read_csv('../data/donneesVoiture.csv')
    operation = ["min", "max", "min", "min", "max", "max", "min"]
    print(weighted_sum(data,operation, "min"))
    display_result(weighted_sum(data,operation, "min"))
    create_graph(weighted_sum(data, operation, "min"), "weighted_sum_voiture")

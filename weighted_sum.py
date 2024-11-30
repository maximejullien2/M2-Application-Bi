import re
import numpy as np
import pandas as pd
import promethee
import networkx as nx
import matplotlib.pyplot as plt
def display(weighted_sum_result, filename):
    plt.clf()
    g = nx.DiGraph()
    for i in range(len(weighted_sum_result) - 1):
        g.add_edge(weighted_sum_result[i],weighted_sum_result[i + 1])
    nx.draw(g, with_labels = True)
    plt.savefig(filename+".png")

def weighted_sum(data, type_operation):
    """
    Launch a weighted sum on a specific data.

    Args:
        data (Panda array): Represente data we want to treat.
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
    result = []
    for i in range(len(columns_name)):
        sum = 0
        for num_line in range(len(data.index)):
            sum += data[columns_name[i]][num_line]*data["TrueWeight"][num_line]
        result.append(sum)
    if type_operation == "max":
        return promethee.sort(result,-1)
    return promethee.sort(result)

data = pd.read_csv('data/donneesFusionerDecher.csv')
print(weighted_sum(data, "min"))
display(weighted_sum(data, "min"),"weighted_sum_decher")
data = pd.read_csv('data/donneesVoiture.csv')
print(weighted_sum(data, "min"))
display(weighted_sum(data, "min"),"weighted_sum_voiture")

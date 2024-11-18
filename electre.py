import re
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def display(matriceDisplay):
    """
    Display the matrix in a png

    Args:
        matriceDisplay list[int][int]: Matrix to display
    """
    g = nx.DiGraph()
    for i in range(len(matriceDisplay)):
        for j in range(len(matriceDisplay)):
            if matriceDisplay[i][j]==1:
                g.add_edge(i, j)
    nx.draw(g, with_labels = True)
    plt.savefig("electre.png")

def compareConcordance(value_x, value_y, weight,operation):
    """
    Compare two value.

    Args:
        value_x (int): Represent value for an instance x on a specific critere.
        value_y (int): Represent value for an instance y on a specific critere.
        weight (int): Represente weight for a specific critere.
        operation (string = "max" or = "min"): Represente operation we want to treat.

    Returns:
        int : Return weight if operation is true or 0 if false.
    """
    if (operation == "min" and value_x < value_y) or (operation == "max" and value_x > value_y):
        return weight
    return 0

def compareDiscordance(value_x, value_y,operation, veto):
    """
    Compare two value.

    Args:
        value_x (int): Represent value for an instance x on a specific critere.
        value_y (int): Represent value for an instance y on a specific critere.
        operation (string = "max" or = "min"): Represente operation we want to treat.

    Returns:
        int : Return weight if operation is true or 0 if false.
    """
    if (operation == "min" and np.absolute(value_y - value_x) >= veto) or (operation == "max" and np.absolute(value_x - value_y) >= veto):
        return 0
    return 1


def compute_electre(data, array_type_operation, veto, seuil):
    """
    Proceed to calculate matrix electre and display in a png the link between attributes

    Args:
        data (pandas.core.frame.DataFrame): The table to treat
        array_type_operation (list[string] = "max" or = "min"): The table checking if how we should treat two data
        veto (int): Value of veto can be increased to reduce the amount of links
        seuil (int): Value of seuil can be increased to reduce the amount of links

    """

    data = pd.read_csv('data/donneesVoiture.csv')
    weightList = table["TrueWeight"].tolist()

    columns_name = []
    for i in data.columns:
        if re.search("^C[0-9]+",i):
            columns_name.append(i)
    matriceComparaison = np.zeros((len(columns_name),len(columns_name)))
    matriceNonDiscordance = np.ones((len(columns_name),len(columns_name)))
    matriceElectreFiltre = np.zeros((len(columns_name),len(columns_name)))

    for i in range(len(columns_name)):
        for j in range(len(columns_name)):
            if i != j:
                sum = 0
                for num_line in range(len(data.index)):
                    if (compareDiscordance(data[columns_name[i]][num_line],data[columns_name[j]][num_line],array_type_operation[num_line], veto[num_line])==0):
                        matriceNonDiscordance[i][j]=0
                    sum += compareConcordance(data[columns_name[i]][num_line],data[columns_name[j]][num_line], data["TrueWeight"][num_line],array_type_operation[num_line])

                matriceComparaison[i][j] = sum
            else:
                matriceNonDiscordance[i][j] = 0

    for i in range(len(columns_name)):
        for j in range(len(columns_name)):
            if (matriceNonDiscordance[i][j]==1 and matriceComparaison[i][j]>=seuil):
                # print(i, j, matriceNonDiscordance[i][j], matriceComparaison[i][j])
                matriceElectreFiltre[i][j]=1

    display(matriceElectreFiltre)


if __name__ == '__main__':
    table = pd.read_csv('data/donneesVoiture.csv')
    vetoTest=[4000, 30, 3, 5, 3, 30, 2]
    compute_electre(table,["min", "max", "min", "min", "max", "max", "min"],vetoTest, 0.5)
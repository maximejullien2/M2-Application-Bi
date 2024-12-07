import re
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def display_result(noyau):
    """
    Display the result of an electre algorithm.
    Args:
        noyau (Array): Represent the noyau of the electre algorithm result.
    """
    print("Voici les meilleurs candidats d'après lalgorithme d'Electre : ",end="")
    for i in noyau:
        print("C"+str(i+1),end=" ")
    print()
def create_graph(matriceDisplay, filename):
    """
    Function to create a graph who will display result of electre algorithm in a filename.
    Args:
        matriceDisplay (Array[Array[]]): Array who represent electre result.
        filename (string): Name of output file.:
    """
    plt.clf()
    g = nx.DiGraph()
    for i in range(len(matriceDisplay)):
        for j in range(len(matriceDisplay)):
            if matriceDisplay[i][j]==1:
                g.add_edge("C"+str(i+1), "C"+str(j+1))
    nx.draw(g, with_labels = True)
    plt.savefig(filename+".png")

def compareConcordance(value_x, value_y, weight,operation, seuil_preference = None):
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
    
    if (operation == "min" and value_x <= value_y) or (operation == "max" and value_x >= value_y):
        return weight
    if seuil_preference != None:
        if (operation == "min" and 0<(value_x - value_y) and (value_x - value_y)<seuil_preference):
            return ((seuil_preference - (value_x - value_y))/seuil_preference) * weight
        elif (operation == "max" and 0<(value_y - value_x) and (value_y - value_x)<seuil_preference):
            return ((seuil_preference - (value_y - value_x))/seuil_preference) * weight
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
    if (operation == "min" and value_x - value_y >= veto) or (operation == "max" and value_y - value_x >= veto):
        return 0
    return 1


def compute_electre(data, array_type_operation, veto, seuil_concordance, seuil_preference = None):
    """
    Proceed to calculate matrix electre and display in a png the link between attributes

    Args:
        data (pandas.core.frame.DataFrame): The table to treat
        array_type_operation (list[string] = "max" or = "min"): The table checking if how we should treat two data
        veto (Array): Value of veto can be increased to reduce the amount of links
        seuil_concordance (int): Value of seuil can be increased to reduce the amount of links
        seuil_preference (Array or None): Array of value of seuil of preference for each categories.

    Returns: 
        array[][] : Return links choosen by electre.
        array[][] : Return concordance array calcuated in electre algorithm.
    """

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
                    seuil = None
                    if seuil_preference != None:
                        seuil = seuil_preference[num_line]
                    if (compareDiscordance(data[columns_name[i]][num_line],data[columns_name[j]][num_line],array_type_operation[num_line], veto[num_line])==0):
                        matriceNonDiscordance[i][j]=0
                    sum += compareConcordance(data[columns_name[i]][num_line],data[columns_name[j]][num_line], data["TrueWeight"][num_line],array_type_operation[num_line], seuil)

                matriceComparaison[i][j] = sum
            else:
                matriceNonDiscordance[i][j] = 0
    for i in range(len(columns_name)):
        for j in range(len(columns_name)):
            if (matriceNonDiscordance[i][j]==1 and matriceComparaison[i][j]>=seuil_concordance):
                matriceElectreFiltre[i][j]=1

    return matriceElectreFiltre, matriceComparaison

def erase_simple_loop(matrix, concordance):
    """
    Proceed to erase where a link between two point can be access by each other.

    Args:
        matrix (Array) : Give each link we use.
        concordance (Array) : Give concordance result wetween two points.

    Returns: 
        array : Return variable matrix without link between two point can be access by each other. 
    """
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i != j and matrix[i][j] == 1 and matrix[j][i] == 1:
                if concordance[i][j] >= concordance[j][i]:
                    matrix[j][i] = 0
                else:
                    matrix[i][j] = 0
    return matrix

def create_graph_without_loop(matrix, concordance, filename):
    """
    Proceed to erase every loop in matrix and after display new graphique.

    Args:
        matrix (Array) : Give each link we use.
        concordance (Array) : Give concordance result wetween two points.

    """
    matrix = erase_simple_loop(matrix, concordance)
    matrix = erase_multi_loop(matrix, concordance)
    create_graph(matrix, filename)
    
def erase_multi_loop(matrix, concordance):
    """
    Proceed to erase any loop in the matrix.

    Args:
        matrix (Array) : Give each link we use.
        concordance (Array) : Give concordance result wetween two points.

    Returns: 
        array : Return variable matrix without any loop. 
    """
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            visiter = []
            if matrix[i][j] == 1:
                fini= False
                visiter.append(i)
                position = j
                ancien = []
                while(fini == False):
                    for x in range(len(matrix)):
                        if (matrix[position][x] == 1 and np.asarray(np.array(matrix) == x).nonzero()):
                            visiter.append(position)
                            position = x
                            break
                    if detect_doublon(visiter):
                        matrix = suppression_noeud(matrix, visiter, concordance)
                        break
                    if len(ancien) != len(visiter):
                        ancien = visiter.copy()
                    else:
                        break
    return matrix
    
def detect_doublon(visiter):
    """
    Detect if a doublon is in array given

    Args:
        visiter (Array) : Array represent each poitn we visit

    Returns: 
        bool : Return if we detect a doublon.
    """
    for j in range(len(visiter) - 1):
        if j != (len(visiter) - 1) and visiter[j] == visiter[len(visiter) - 1]:
            return True
    return False

def suppression_noeud(matrix, visiter, concordance):
    """
    Proceed to erase a link in a loop detected.

    Args:
        matrix (Array) : Give each link we use.
        visiter (Array) : Represent each point we visit
        concordance (Array) : Give concordance result wetween two points.

    Returns: 
        array : Return variable matrix without the loop detected. 
    """
    while True:
        if visiter[0] != visiter[len(visiter) - 1]:
            visiter.pop(0)
        else : 
            break
    noeud = []
    mininmum = 999999
    for i in range(len(visiter)-1):
        if mininmum > concordance[visiter[i]][visiter[i+1]]:
            mininmum = concordance[visiter[i]][visiter[i+1]]
            noeud = [visiter[i], visiter[i+1]]
    matrix[noeud[0]][noeud[1]] = 0
    return matrix

def get_noyaux(matrix,concordance):
    """
    Get noyaux from electre result.
    Args:
        matrix (Array) : Give each link we use.
        concordance (Array) : Give concordance result wetween two points.

    Returns:
        array : Return noyau of electre result.
    """
    matrix = erase_simple_loop(matrix, concordance)
    matrix = erase_multi_loop(matrix, concordance)
    visiter = np.ones(len(matrix[0]))
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix[0])):
            if matrix[i][j] == 1:
                visiter[j] = 0
    noyau = []
    for i in range(len(visiter)):
        if visiter[i] == 1:
            noyau.append(i)
    return noyau


if __name__ == '__main__':
    data = pd.read_csv('../data/donneesFusionerDecher.csv')
    min = []
    veto = []
    seuil_preference = []
    seuil_concordance = 0
    for i in range(0,data.index.size):
        min.append("min")
        veto.append(10)
        seuil_preference.append(2)


    matriceElectreFiltre, matriceComparaison = compute_electre(data, min, veto, seuil_concordance)
    get_noyaux(matriceElectreFiltre, matriceComparaison)
    create_graph_without_loop(matriceElectreFiltre, matriceComparaison, "ElectreIV_dechet")

    matriceElectreFiltre, matriceComparaison = compute_electre(data, min, veto, seuil_concordance,seuil_preference)
    get_noyaux(matriceElectreFiltre, matriceComparaison)
    create_graph_without_loop(matriceElectreFiltre, matriceComparaison, "ElectreIS_dechet")

    data = pd.read_csv('../data/donneesVoiture.csv')
    operation = ["min", "max", "min", "min", "max", "max", "min"]
    veto = [3000, 69, 2, 4, 3, 50, 2]
    seuil_preference = [500, 20, 1, 2, 1.5, 20, 0.5]
    seuil_concordance = 0.5

    matriceElectreFiltre, matriceComparaison = compute_electre(data, min, veto, seuil_concordance)
    get_noyaux(matriceElectreFiltre, matriceComparaison)
    create_graph_without_loop(matriceElectreFiltre, matriceComparaison, "ElectreIV_voiture")

    matriceElectreFiltre, matriceComparaison = compute_electre(data, min, veto, seuil_concordance,seuil_preference)
    get_noyaux(matriceElectreFiltre, matriceComparaison)
    create_graph_without_loop(matriceElectreFiltre, matriceComparaison, "ElectreIS_voiture")

import re
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt



def display(matriceDisplay, filename):
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
        value = 0
        if (operation == "min" and 0<(value_x - value_y) and (value_x - value_y)<seuil_preference):
            return (((value_x - value_y)- seuil_preference)/seuil_preference) * weight
        elif (operation == "max" and 0<(value_y - value_x) and (value_y - value_x)<seuil_preference):
            return (((value_y - value_x)- seuil_preference)/seuil_preference) * weight
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
                # print(i, j, matriceNonDiscordance[i][j], matriceComparaison[i][j])
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

def display_without_loop(matrix, concordance):
    """
    Proceed to erase every loop in matrix and after display new graphique.

    Args:
        matrix (Array) : Give each link we use.
        concordance (Array) : Give concordance result wetween two points.

    """
    matrix = erase_simple_loop(matrix, concordance)
    matrix = erase_multi_loop(matrix, concordance)
    display(matrix)
    
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
        visiter (Array) : Represent each poitn we visit
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
                    


if __name__ == '__main__':
    table = pd.read_csv('data/donneesVoiture.csv')
    vetoTest=[4000, 30, 3, 5, 3, 30, 2]
    matrix = [[0,0,1,1],[1,0,0,0],[0,1,0,1],[0,1,1,0]]
    concordance = [[0,0,0.4,0.5],[0.6,0,0,0],[0,0.7,0,0.8],[0,0.9,1,0]]
    display_without_loop(matrix, concordance)
    #compute_electre(table,["min", "max", "min", "min", "max", "max", "min"],vetoTest, 0.5)
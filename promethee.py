import re
import numpy as np
import pandas as pd
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
        for i in range(len(array_sort)):
            empty.append(array_sort[len(array_sort) - i -1])
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


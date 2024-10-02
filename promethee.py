import re
import numpy as np
def comparaison(value_x, value_y, weight,operation):
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

def promethee(selection_mode, data, array_type_operation):
    """
    Launch a specific Promethee.

    Args:
        selection_mode (int = 1 or = 2): Select Promethee.
        data (Panda array): Represente data we want to treat.
        array_type_operation (array): Represente action we want to do on each critère ("min" ou "max").

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
        
        if data == None: 
            raise ValueError("Data value is None")
        
    except ValueError as err :
        print(err.args[0])
        exit(0)
    columns_name = []
    for i in data.columns:
        if re.search("^C[0-9]*",i):
            columns_name.append(i)
    table_degres_preference_multicritere = np.zeros((len(columns_name), len(columns_name)))


    



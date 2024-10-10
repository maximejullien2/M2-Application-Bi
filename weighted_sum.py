import re
import numpy as np
import pandas as pd
import promethee
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
        if type_operation[i] != "max" and type_operation[i] != "min":
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

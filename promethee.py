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
    """
    try:
        if selection_mode > 2 or selection_mode <= 0 : 
            raise ValueError("Type of Promethee need to be 1 or 2")
        
        for i in range(len(array_type_operation)):
            if array_type_operation[i] != "max" and array_type_operation[i] != "min":
                raise ValueError(f"At indice {i} , the array array_type_operation have a data different from 'min' or 'max'.")
        
        if data == None: 
            raise ValueError("Data value is None")
        
    except ValueError as err :
        print(err.args[0])
        exit(0)

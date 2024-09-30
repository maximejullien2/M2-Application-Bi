def promethee(selection_mode, data , weight):
    """
    Réalise le promethee sélectionné.

    Args:
        selection_mode (int = 1 ou = 2): Choisi le type de Promethee que l'on veut sélectionner.
        data (Panda array): Représente les données que l'on va traiter.
        weight (Panda array): Représente les poids des différents critères.

    Returns:
        Array_list : Retourne la liste des meilleurs éléments

    Raises:
            ValueError: Si selection_mode > 2 ou == 0.
    """
    try:
        if selection_mode > 2 or selection_mode == 0 : 
            raise ValueError("Le Type de Promethee est soit 1 ou 2")
    except ValueError as err :
        print(err.args[0])
        exit(0)

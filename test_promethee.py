import promethee
import parseur
import pandas as pd 

if __name__ == '__main__':
    table = pd.read_csv('data/promethe.csv')

    print("Résultat de Promethee I sans seuil:")
    print("A obtenir : [array([4, 2, 5, 3, 1, 0]), array([4, 2, 3, 5, 1, 0])] , Obtenu :", promethee.promethee(1, table,["min", "max", "min", "min", "min", "max"]))
    print("Résultat de Promethee II sans seuil:")
    print("A obtenir : [4 2 3 5 1 0] , Obtenu :",promethee.promethee(2, table,["min", "max", "min", "min", "min", "max"]),"\n")
    print("Résultat de Promethee I sans seuil:")
    print("A obtenir : [array([4, 1, 3, 5, 2, 0]), array([4, 5, 2, 1, 3, 0])] , Obtenu :",promethee.promethee_seuil(1, table, [20, 10, 200, 4, 2, 2],["min", "max", "min", "min", "min", "max"]))
    print("Résultat de Promethee II sans seuil:")
    print("A obtenir : [4 5 1 2 3 0] , Obtenu :",promethee.promethee_seuil(2, table, [20, 10, 200, 4, 2, 2],["min", "max", "min", "min", "min", "max"]),"\n")
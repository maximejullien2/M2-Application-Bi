import weighted_sum
import pandas as pd
if __name__ == '__main__':
    table = pd.read_csv('data/weighted_sum.csv')
    print("Résultat de la somme pondérée : ")
    print("A obtenir : [2 0 1 3] , Obtenu : ",weighted_sum.weighted_sum(table,"max"))


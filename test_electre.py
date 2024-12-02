import electre
import parseur
import pandas as pd

def affichage_matriceComparaison(i, matriceComparaison):
    if i == 0:
        print("[", end="")
    print("[", end="")
    for j in range(len(matriceComparaison[i])):
        print(str('%.4f' % matriceComparaison[i][j]), end="")
        if j != len(matriceComparaison[i])-1:
            print(", ", end="")
    if i < len(matriceComparaison) - 1:
        print("],  | ", end="")
    else:
        print("]]  | ", end="")

def affichage_matriceElectreFiltre(i , matriceElectreFiltre):
    if i == 0:
        print("[", end="")
    print("[", end="")
    for j in range(len(matriceElectreFiltre[i])):
        print(str('%.0f' % matriceElectreFiltre[i][j]), end="")
        if j != len(matriceElectreFiltre[i])-1:
            print(", ", end="")
    if i < len(matriceElectreFiltre) - 1:
        print("],")
    else:
        print("]]")
def affichage(matriceElectreFiltre, matriceComparaison):
    print("Obtenue : ")
    print("Matrice de concordance                             | Matrice de non-discordance ")
    for i in range(len(matriceElectreFiltre)):
        affichage_matriceComparaison(i, matriceComparaison)
        affichage_matriceElectreFiltre(i, matriceElectreFiltre)
if __name__ == '__main__':
    table = pd.read_csv('data/promethe.csv')

    print("Résultat de Electre Iv:")

    matriceElectreFiltre, matriceComparaison = electre.compute_electre( table, ["min", "max", "min", "min", "min", "max"], [45, 29, 550, 6, 4.5, 4.5], 0.6, None)
    affichage(matriceElectreFiltre, matriceComparaison)

    print("Résultat de Electre Is:")

    matriceElectreFiltre, matriceComparaison = electre.compute_electre( table, ["min", "max", "min", "min", "min", "max"], [45, 29, 550, 6, 4.5, 4.5], 0.6, [20, 10, 200, 4, 2, 2])
    affichage(matriceElectreFiltre, matriceComparaison)
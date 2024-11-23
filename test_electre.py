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
    print("A obtenir : "+"\n"+
          "Matrice de concordance                             | Matrice de non-discordance "+"\n"+
          "[[0.0000, 0.5000, 0.4000, 0.5000, 0.4000, 0.3000], | [[0, 0, 0, 0, 0, 0], "+"\n"+
          "[0.5000, 0.0000, 0.5000, 0.4000, 0.4000, 0.5000],  | [0, 0, 0, 0, 0, 0], " + "\n" +
          "[0.6000, 0.5000, 0.0000, 0.5000, 0.2000, 0.7000],  | [0, 0, 0, 0, 0, 0], " + "\n" +
          "[0.5000, 0.6000, 0.5000, 0.0000, 0.5000, 0.3000],  | [0, 0, 0, 0, 0, 0], " + "\n" +
          "[0.8000, 0.6000, 0.8000, 0.5000, 0.0000, 0.8000],  | [1, 1, 1, 0, 0, 1], " + "\n" +
          "[0.7000, 0.5000, 0.3000, 0.7000, 0.2000, 0.0000]]  | [1, 0, 0, 0, 0, 0]] " + "\n")

    matriceElectreFiltre, matriceComparaison = electre.compute_electre( table, ["min", "max", "min", "min", "min", "max"], [45, 29, 550, 6, 4.5, 4.5], 0.6, None)
    affichage(matriceElectreFiltre, matriceComparaison)

    print("Résultat de Electre Is:")
    print("A obtenir : " + "\n" +
          "Matrice de concordance                              | Matrice de non-discordance " + "\n" +
          "[[0.0000, 0.525, 0.4000, 0.6000, 0.4150, 0.5350],   | [[0, 0, 0, 0, 0, 0], " + "\n" +
          "[0.5000, 0.0000, 0.6975, 0.4445, 0.4350, 0.5000],   | [0, 0, 0, 0, 0, 0], " + "\n" +
          "[0.7400, 0.5100, 0.0000, 0.5000, 0.4000, 0.7100],   | [0, 0, 0, 0, 0, 0], " + "\n" +
          "[0.5475, 0.6000, 0.5925, 0.0000, 0.5000, 0.3025],   | [0, 0, 0, 0, 0, 0], " + "\n" +
          "[0.8000, 0.6000, 0.8000, 0.5800, 0.0000, 0.8000],   | [1, 1, 1, 0, 0, 1], " + "\n" +
          "[0.8300, 0.5000, 0.5450, 0.7000, 0.3600, 0.0000]]   | [1, 0, 0, 0, 0, 0]] " + "\n")

    matriceElectreFiltre, matriceComparaison = electre.compute_electre( table, ["min", "max", "min", "min", "min", "max"], [45, 29, 550, 6, 4.5, 4.5], 0.6, [20, 10, 200, 4, 2, 2])
    affichage(matriceElectreFiltre, matriceComparaison)
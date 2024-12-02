import electre
import promethee
import pandas as pd
from electre import *
#from test_electre import *
import ast
import weighted_sum
from test_electre import affichage
import borda


def miniParseur(min_path):
    if min_path == None:
        return None
    try:
        min_list = []

        with open(min_path, 'r') as file:
            for line in file:
                line = line.strip()
                min_list.append(line)
        return min_list
    except FileNotFoundError:
        print(f"Le fichier à l'emplacement {min_path} est introuvable.")
        return
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return


def main():
    fonction = input("Entrez le nom de la fonction (ex : electre, promethee, weightsum, borda): ")

    fichier_path = input("Entrez le chemin du fichier : ")

    min_path = input("Entrez le chemin vers le fichier contenant les operations min/max : ")
    min_list = miniParseur(min_path)

    print(f"Nom de la fonction : {fonction}")
    print(f"Chemin du fichier : {fichier_path}")
    print(f"Liste des operations : {min_list}")

    data = pd.read_csv(fichier_path)
    if (fonction == "promethee"):
        versionProme = input("Choisiser entre promethee '1' ou '2' (ex: 1) : ")

        listeSeuil=None
        listeSeuil_path = input("OPTIONEL: Entrez le chemin vers le fichier contenant les seuils : ")
        listeSeuil=miniParseur(listeSeuil_path)
        for i in range(len(listeSeuil)):
            listeSeuil[i]=int(listeSeuil[i])

        if (versionProme=="1"):
            print(promethee.promethee(1, data, min_list, listeSeuil))
            promethee.display(1, promethee.promethee(1, data, min_list, listeSeuil), "Promethee1")
        else:
            print(promethee.promethee(2, data, min_list, listeSeuil))
            promethee.display(2, promethee.promethee(2, data, min_list, listeSeuil), "Promethee2")


    if (fonction == "electre"):
        veto_path = input("Entrez le chemin vers le fichier contenant les vetos : ")
        vetoList=miniParseur(veto_path)
        vetoList=list(map(int, vetoList))
        concordance = input("Entrez le numero de concordance : ")
        concordance = float(concordance)
        listeSeuil=None
        listeSeuil_path = input("Pour Electre Is (optionel): Entrez le chemin vers le fichier contenant les seuils : ")
        listeSeuil = miniParseur(listeSeuil_path)

        matriceElectreFiltre, matriceComparaison = electre.compute_electre(data,min_list,vetoList,concordance, listeSeuil)
        electre.get_noyaux(matriceElectreFiltre, matriceComparaison)
        electre.display_without_loop(matriceElectreFiltre, matriceComparaison, "Electre")

        affichage(matriceElectreFiltre, matriceComparaison)

    if (fonction == "weightsum"):
        opera = input("Entrez le nom de l'operation min ou max (sans guillemet) : ")
        print(weighted_sum.weighted_sum(data, min_list, opera))
        weighted_sum.display(weighted_sum.weighted_sum(data, min_list, opera), "weighted_sum")

    if (fonction == "borda"):
        print(borda.borda(data, min_list))
        borda.display(borda.borda(data, min_list))




if __name__ == "__main__":
    main()

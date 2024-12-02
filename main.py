import electre
import promethee
import pandas as pd
from electre import *
#from test_electre import *
import ast

from test_electre import affichage


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
    fonction = input("Entrez le nom de la fonction (ex : electre, promethee): ")

    fichier_path = input("Entrez le chemin du fichier : ")

    print(f"Nom de la fonction : {fonction}")
    print(f"Chemin du fichier : {fichier_path}")

    data = pd.read_csv(fichier_path)
    if (fonction == "promethee"):
        min_path = input("Entrez le chemin vers le fichier contenant les operations min/max : ")
        min_list=miniParseur(min_path)
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
        min_path = input("Entrez le chemin vers le fichier contenant les operations min/max : ")
        min_list=miniParseur(min_path)
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




if __name__ == "__main__":
    main()

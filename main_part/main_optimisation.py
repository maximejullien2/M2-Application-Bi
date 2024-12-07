from function import promethee, borda, weighted_sum, electre
import argparse
import pandas as pd
import os

def miniParseur(min_path):
    """
    Parse data in file.
    Args:
        min_path: Represent file we want to parse.
    Returns:
        Array[str]: Array who contain data of min_path.
    """
    if min_path == "":
        return None
    try:
        min_list = []

        with open(min_path, 'r') as file:
            for line in file:
                line = line.strip()
                min_list.append(line)
        return min_list
    except FileNotFoundError:
        exit(f"Le fichier à l'emplacement {min_path} est introuvable.")
    except Exception as e:
        exit(f"Une erreur est survenue : {e}")


def main():
    """
    Parsing main part of the program.

    """
    if ("output" in os.listdir("../")) == False:
        os.mkdir("./output")
    args = parse_arguments()
    fonction = input(
        "Entrez le nom de la fonction (ex : electre, promethee, weightsum, borda): ") if args.function == "" else args.function
    if (fonction in ["electre", "promethee", "weightsum", "borda"]) == False:
        while True:
            fonction = input(
                "Entrez le nom de la fonction (ex : electre, promethee, weightsum, borda): ")
            if fonction in ["electre", "promethee", "weightsum", "borda"]:
                break

    fichier_path = input("Entrez le chemin du fichier : ") if args.filepath == "" else args.filepath
    try:
        file = open(fichier_path, "r")
        file.close()
    except FileNotFoundError:
        exit(f"Le fichier à l'emplacement {fichier_path} est introuvable.")

    min_path = input(
        "Entrez le chemin vers le fichier contenant les operations min/max : ") if args.operation == "" else args.operation
    min_list = miniParseur(min_path)

    print(f"Nom de la fonction : {fonction}")
    print(f"Chemin du fichier : {fichier_path}")
    print(f"Liste des operations : {min_list}")

    data = pd.read_csv(fichier_path)
    if fonction == "promethee":
        versionProme = input(
            "Choisiser entre promethee '1' ou '2' (ex: 1) : ") if args.version_algorithme == "" else args.version_algorithme
        if versionProme != "1" and versionProme != "2":
            while True:
                versionProme = input(
                    "Choisiser entre promethee '1' ou '2' (ex: 1) : ")
                if versionProme == "1" or versionProme == "2":
                    break

        listeSeuil = None
        listeSeuil_path = None
        if args.seuil == "":
            listeSeuil_path = input("OPTIONEL: Entrez le chemin vers le fichier contenant les seuils : ")
        elif args.seuil != "None":
            listeSeuil_path = args.seuil
        print(listeSeuil_path)
        listeSeuil = miniParseur(listeSeuil_path)
        if listeSeuil is not None:
            for i in range(len(listeSeuil)):
                listeSeuil[i] = float(listeSeuil[i])

        if versionProme == "1":
            result = promethee.promethee(1, data, min_list, listeSeuil)
            promethee.display_result(1, result)
            promethee.create_graph(1, result, "./output/PrometheeI")
        else:
            result = promethee.promethee(2, data, min_list, listeSeuil)
            promethee.display_result(2, result)
            promethee.create_graph(2, result, "./output/PrometheeII")

    elif fonction == "electre":
        veto_path = input(
            "Entrez le chemin vers le fichier contenant les vetos : ") if args.veto == "" else args.veto
        vetoList = miniParseur(veto_path)
        vetoList = list(map(int, vetoList))
        concordance = input(
            "Entrez un seuil de concordance compris entre 0 et 1: ") if args.concordance == "" else args.concordance
        concordance = float(concordance)
        while concordance < 0 or concordance > 1:
            concordance = input("Entrez un seuil de concordance compris entre 0 et 1: ")
            concordance = float(concordance)
        listeSeuil = None
        listeSeuil_path = None
        if args.seuil == "":
            listeSeuil_path = input(
                "Pour Electre Is (optionel): Entrez le chemin vers le fichier contenant les seuils : ")
        elif args.seuil != "None":
            listeSeuil_path = args.seuil
        listeSeuil = miniParseur(listeSeuil_path)
        if listeSeuil is not None:
            for i in range(len(listeSeuil)):
                listeSeuil[i] = float(listeSeuil[i])

        matriceElectreFiltre, matriceComparaison = electre.compute_electre(data, min_list, vetoList, concordance,
                                                                           listeSeuil)
        noyau = electre.get_noyaux(matriceElectreFiltre, matriceComparaison)
        electre.create_graph_without_loop(matriceElectreFiltre, matriceComparaison, "./output/Electre")
        electre.display_result(noyau)

    elif fonction == "weightsum":
        opera = input(
            "Entrez le nom de l'operation min ou max (sans guillemet) : ") if args.type_result == "" else args.type_result
        if opera != "max" and opera != "min":
            while True:
                opera = input(
                    "Entrez le nom de l'operation min ou max (sans guillemet) : ")
                if opera != "max" and opera != "min":
                    break

        result = weighted_sum.weighted_sum(data, min_list, opera)
        weighted_sum.display_result(result)
        weighted_sum.create_graph(result, "./output/weighted_sum")

    elif fonction == "borda":
        result = borda.borda(data, min_list)
        borda.display_result(result)
        borda.create_graph(result, "./output/borda")



def parse_arguments() -> argparse.Namespace:
    """
    Represente argument we will use for this part of the program.

    Returns:
        argparse.Namespace : Will let you retrieve data send from the command line.
    """
    parser = argparse.ArgumentParser(description="Réaliser la méthodologie d'optimisation sélectionné")
    parser.add_argument("-type", default="")

    parser.add_argument("-f", "--function", default="", help="Définis le type d'optimisation que l'on va faire (borda, promethee, electre ou weightsum")
    parser.add_argument("-file", "--filepath", default="", help="Définie sur quel fichier on veut réaliser le travail")
    parser.add_argument("-op", "--operation", default="", help="Définie sur quel fichier on se trouvera le type d'operation que l'on veut apr critère ( min ou max)")
    parser.add_argument("-type_result", default="", help="Pour la weightsum savoir pour quel ordre on veut que la sortie soit (min pour ordre croissant , max par ordre décroissant")

    parser.add_argument("-v", "--version_algorithme", default="", help="Pour Prométhée , savoir lequel on va utiliser (1 pour PromethéeI ou 2 pour ProméthéeII)")
    parser.add_argument("-concordance", default="", help="Représente le seuil de concordance compris entre 0 et 1")
    parser.add_argument("-seuil", default="" ,help="Définie quel fichier on va utiliser pour récupérer les seuil de préférence pour Electre et Prométhee")
    parser.add_argument("-veto", default="" ,help="Définie quel fichier on va utiliser pour récupérer les vetos pour Electre.")
    return parser.parse_args()



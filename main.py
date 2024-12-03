import borda
import electre
import promethee
import weighted_sum
import argparse
from electre import *
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


def main(args: argparse.Namespace):
    if args.type == "optimisation":

        fonction = input(
            "Entrez le nom de la fonction (ex : electre, promethee, weightsum, borda): ") if args.function == "" else args.function

        fichier_path = input("Entrez le chemin du fichier : ") if args.filepath == "" else args.filepath

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

            listeSeuil = None
            listeSeuil_path = None
            if args.seuil == "":
                listeSeuil_path = input("OPTIONEL: Entrez le chemin vers le fichier contenant les seuils : ")
            elif args.seuil != "None":
                listeSeuil_path = args.seuil
            listeSeuil = miniParseur(listeSeuil_path)
            if listeSeuil is not None:
                for i in range(len(listeSeuil)):
                    listeSeuil[i] = float(listeSeuil[i])

            if versionProme == "1":
                print(promethee.promethee(1, data, min_list, listeSeuil))
                promethee.display(1, promethee.promethee(1, data, min_list, listeSeuil), "Promethee1")
            else:
                print(promethee.promethee(2, data, min_list, listeSeuil))
                promethee.display(2, promethee.promethee(2, data, min_list, listeSeuil), "Promethee2")

        if fonction == "electre":
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
            electre.get_noyaux(matriceElectreFiltre, matriceComparaison)
            electre.display_without_loop(matriceElectreFiltre, matriceComparaison, "Electre")

            affichage(matriceElectreFiltre, matriceComparaison)

        if fonction == "weightsum":
            opera = input(
                "Entrez le nom de l'operation min ou max (sans guillemet) : ") if args.type_result == "" else args.type_result
            print(weighted_sum.weighted_sum(data, min_list, opera))
            weighted_sum.display(weighted_sum.weighted_sum(data, min_list, opera), "weighted_sum")

        if fonction == "borda":
            print(borda.borda(data, min_list))
            borda.display(borda.borda(data, min_list))


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("type")
    parser.add_argument("-f", "--function", default="")

    parser.add_argument("-file", "--filepath", default="")
    parser.add_argument("-op", "--operation", default="")
    parser.add_argument("-type_result", default="")

    parser.add_argument("-v", "--version_algorithme", default="")
    parser.add_argument("-concordance", default="")
    parser.add_argument("-seuil", default="")
    parser.add_argument("-veto", default="")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

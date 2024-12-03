import borda
import electre
import parseur
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
    elif args.type == "parseur":
        fichier_path = input("Entrez le chemin du fichier : ") if args.filepath == "" else args.filepath
        data = pd.read_csv(fichier_path)
        if args.transpose or input("Voulez-vous transposé vos données ? (y/n) : ") == "y":
            data = data.transpose()
        if args.data_type or input(
                "Voulez-vous que les colonnes soit nommées (le programme à besoin d'une nommation spécifique) ? (y/n) : ") == "y":
            array = []
            for i in range(1, len(data.columns) + 1):
                array.append(f"C{i}")
            data.set_axis(array, axis=1)
        if args.categorie != None:
            for i in range(len(args.categorie)):
                liste = miniParseur(args.categorie[i])
                if liste is not None:
                    for j in range(len(liste)):
                        liste[j] = float(liste[j])
                data.insert(0, args.categorie_name[i], liste)
        if args.weight != "" or input("Donner un fichier Weight celon les critère si vous le souhaitez : ") != "":
            liste = miniParseur(args.weight)
            if liste is not None:
                for j in range(len(liste)):
                    liste[j] = float(liste[j])
            data.insert(0, "Weight", liste)
        if args.true_weight != "" or input(
                "Donner un fichier TrueWeight celon les critère si vous le souhaitez : ") != "":
            liste = miniParseur(args.true_weight)
            if liste is not None:
                for j in range(len(liste)):
                    liste[j] = float(liste[j])
            data.insert(0, "TrueWeight", liste)
        if args.compute_true_weight or input(
                "Voulez-vous qu'on calcul la True Weight par rapport au Weight et au Catégories : (y/n) ") == "y":
            data = parseur.computeTrueWeight(data, "")
        if args.compute_true_weight_filtered != None:
            data = parseur.computeTrueWeightFiltered(data, args.compute_true_weight_filtered, "")
        data.to_csv(args.output + ".csv", index=False)

    else:
        exit(f"L'option {args.type} n'est pas connu")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("type")
    parser.add_argument("output")
    parser.add_argument("-transpose", action=argparse.BooleanOptionalAction)
    parser.add_argument("-data_type", action=argparse.BooleanOptionalAction)
    parser.add_argument("-categorie", action="append")
    parser.add_argument("-categorie_name", action="append")
    parser.add_argument("-compute_true_weight", action=argparse.BooleanOptionalAction)
    parser.add_argument("-compute_true_weight_filtered", nargs='+')
    parser.add_argument("-true_weight", default="")
    parser.add_argument("-weight", default="")

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

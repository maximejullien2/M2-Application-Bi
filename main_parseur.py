import parseur
import argparse
import pandas as pd

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
    args = parse_arguments()
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

    output = input(
        "Entrez le path de sortie du programme ") if args.output == "" else args.output

    data.to_csv(output, index=False)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Permet de modifier les données afin de pouvoir les utiliser pour la aprtie optimisation")
    parser.add_argument("-type",default="")
    parser.add_argument("-output", help="Représente la sortie du programme")
    parser.add_argument("-transpose", action=argparse.BooleanOptionalAction ,help="Représente si on doit transposé les données")
    parser.add_argument("-data_type", action=argparse.BooleanOptionalAction, help="Représente si on doit créer les colonnes C* nécessaire pour la partie optimisation")
    parser.add_argument("-categorie", action="append" ,help="Représente le fichier ou les donénes se trouve de la catégorie que l'on veut ajoute")
    parser.add_argument("-categorie_name", action="append", help = "Représente le nom de la colonne que l'on veut ajouter.")
    parser.add_argument("-compute_true_weight", action=argparse.BooleanOptionalAction, help ="Défini si on doit calculer la TrueWeight par rapport a la colonne Catégorie et à la colonne Weight")
    parser.add_argument("-compute_true_weight_filtered", nargs='+',help="Défini quel catégorie on veut traiter dans la Colonne catégorie lors du calcul de la TrueWeight")
    parser.add_argument("-true_weight", default="", help="Représente le fichier ou se trouve les TrueWeight que l'on va rajouter au donnée")
    parser.add_argument("-weight", default="", help="Représente le fichier ou se trouve les TrueWeight que l'on va rajouter au donnée")

    parser.add_argument("-file", "--filepath", default="", help="Défini sur quel fichier on veut réaliser ces traitements")
    return parser.parse_args()

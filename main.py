import argparse
import main_parseur
import main_optimisation
import sys
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
    if len(sys.argv)>1:
        if sys.argv[1] == '-h':
            exit("usage: main.py [-h] type"+"\n"+
            "Choisir le type de travail que l'on veut faire"+"\n\n"+
            "positional arguments:"+"\n"+
            "  type        optimisation ou parseur"+"\n\n"+
            "options:"+"\n"+
            "  -h, --help  show this help message and exit")
        if sys.argv[1] == "optimisation":
            main_optimisation.main()
        elif sys.argv[1] == "parseur":
            main_parseur.main()
        else:
            exit(f"L'option {sys.argv[1]} n'est pas connu")
    else:
        while True:
            type = input("Définit le type de travail que l'on veut faire (optimisation ou parseur): ")
            if type.lower() == "optimisation" or type.lower() == "parseur":
                type = type.lower()
                break
        if type == "optimisation":
            main_optimisation.main()
        elif type == "parseur":
            main_parseur.main()


if __name__ == "__main__":
    main()

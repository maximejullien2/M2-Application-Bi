from main_part import main_optimisation, main_parseur
import sys

def main():
    """
    Main function of program. You will select the task of the program ( optimisation or parseur)
    """
    if len(sys.argv)>1:
        if sys.argv[1] == '-h':
            exit("usage: main.py [-h] [-type]"+"\n"+
            "Permet de réaliser le type de travail que l'on veut produire."+"\n\n"+
            "options:"+"\n"+
            "  -type  type     optimisation ou parseur"+"\n"+
            "  -h, --help      montre ce message d'aide puis arrète le program")
        if sys.argv[1] == "-type":
            if sys.argv[2] == "optimisation":
                main_optimisation.main()
            elif sys.argv[2] == "parseur":
                main_parseur.main()
            else:
                exit(f"L'option {sys.argv[2]} n'est pas connu")
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

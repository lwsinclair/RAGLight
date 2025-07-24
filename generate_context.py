import os

import subprocess

import argparse

import sys

 

def run_tree_command(directory, depth, output_file):

    """

    Exécute la commande 'tree' et écrit la sortie dans un fichier.

    Retourne True en cas de succès, False sinon.

    """

    command = ["tree", "-L", str(depth), directory]

    print(f"Exécution de la commande : {' '.join(command)}")

    try:

        # Exécute la commande et capture la sortie

        result = subprocess.run(

            command,

            capture_output=True,

            text=True, # Décode stdout/stderr en texte (UTF-8 par défaut)

            check=True, # Lève une exception si la commande échoue

            encoding='utf-8' # Spécifie l'encodage explicitement

        )

 

        # Écrit la sortie dans le fichier MD (mode 'w' pour écraser)

        with open(output_file, 'w', encoding='utf-8') as f:

            f.write(f"# Arborescence du répertoire '{os.path.basename(directory)}' (Profondeur {depth})\n\n")

            f.write("```\n")

            f.write(result.stdout)

            f.write("```\n\n")

        print(f"Sortie de 'tree' écrite dans '{output_file}'")

        return True

 

    except FileNotFoundError:

        print(f"Erreur : La commande 'tree' n'a pas été trouvée. Est-elle installée et dans le PATH ?", file=sys.stderr)

        return False

    except subprocess.CalledProcessError as e:

        print(f"Erreur lors de l'exécution de 'tree': {e}", file=sys.stderr)

        print(f"Stderr: {e.stderr}", file=sys.stderr)

        return False

    except Exception as e:

        print(f"Une erreur inattendue est survenue lors de l'exécution de tree: {e}", file=sys.stderr)

        return False

 

def append_python_files(directory, output_file):

    """

    Parcourt le répertoire, trouve les fichiers .py et ajoute leur contenu au fichier MD.

    """

    print(f"Recherche des fichiers Python dans '{directory}'...")

    found_files = False

    try:

        # Ouvre le fichier MD en mode 'a' (append)

        with open(output_file, 'a', encoding='utf-8') as md_file:

            md_file.write("# Contenu des fichiers Python\n\n")

 

            # Parcourt récursivement le répertoire

            for root, _, files in os.walk(directory):

                for filename in files:

                    if filename.endswith(".py"):

                        found_files = True

                        file_path = os.path.join(root, filename)

                        # Calcule le chemin relatif par rapport au répertoire de base

                        relative_path = os.path.relpath(file_path, directory)

                        print(f"  Ajout du fichier : {relative_path}")

 

                        try:

                            # Lit le contenu du fichier Python

                            with open(file_path, 'r', encoding='utf-8') as py_file:

                                content = py_file.read()

 

                            # Ajoute au fichier MD

                            md_file.write(f"**{relative_path}**\n\n")

                            md_file.write("```python\n")

                            md_file.write(content)

                            md_file.write("\n```\n\n")

 

                        except Exception as e:

                            print(f"  Erreur lors de la lecture du fichier '{file_path}': {e}", file=sys.stderr)

                            md_file.write(f"**{relative_path}**\n\n")

                            md_file.write(f"```\nErreur lors de la lecture du fichier : {e}\n```\n\n")

 

        if not found_files:

            print("Aucun fichier .py trouvé.")

        else:

            print(f"Contenu des fichiers Python ajouté à '{output_file}'")

 

    except Exception as e:

        print(f"Erreur lors de l'écriture dans le fichier '{output_file}': {e}", file=sys.stderr)

 

def main():

    parser = argparse.ArgumentParser(

        description="Génère un fichier Markdown avec l'arborescence d'un répertoire et le contenu de ses fichiers Python."

    )

    parser.add_argument(

        "directory",

        help="Le chemin vers le répertoire à analyser."

    )

    parser.add_argument(

        "-d", "--depth",

        type=int,

        default=3,

        help="La profondeur maximale pour la commande 'tree' (défaut: 3)."

    )

    parser.add_argument(

        "-o", "--output",

        default="output.md",

        help="Le nom du fichier Markdown de sortie (défaut: output.md)."

    )

 

    args = parser.parse_args()

 

    # Vérifie si le répertoire existe

    if not os.path.isdir(args.directory):

        print(f"Erreur : Le répertoire '{args.directory}' n'existe pas ou n'est pas un répertoire.", file=sys.stderr)

        sys.exit(1)

 

    # Étape 1: Exécuter tree et écrire la sortie

    if run_tree_command(args.directory, args.depth, args.output):

        # Étape 2: Parcourir les fichiers Python et ajouter leur contenu

        append_python_files(args.directory, args.output)

        print("\nTerminé !")

    else:

        print("\nScript arrêté en raison d'erreurs lors de l'exécution de 'tree'.")

        sys.exit(1)

 

if __name__ == "__main__":

    main()

 
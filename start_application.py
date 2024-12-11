import os
import subprocess
import time
from colorama import Fore, init
from tqdm import tqdm  # Pour afficher une barre de progression

# Initialisation de colorama (nécessaire pour Windows)
init(autoreset=True)


def update_pip():
    """
    Met à jour `pip` à la dernière version disponible avec un écran de chargement.
    """
    print(f"{Fore.RED}=========== Mise à jour de pip ============\n")
    with open(os.devnull, 'w') as fnull:
        with tqdm(total=1, desc="Mise à jour de pip", ncols=80) as pbar:
            subprocess.run(
                ["python", "-m", "pip", "install", "--upgrade", "pip"],
                stdout=fnull,
                stderr=fnull,
                check=True
            )
            pbar.update(1)


def install_dependencies():
    """
    Installe les dépendances nécessaires pour le projet à partir du fichier requirements.txt.
    Affiche une barre de progression pendant le processus.
    """
    print(f"{Fore.RED}=========== Installation des dépendances ============\n")
    with open(os.devnull, 'w') as fnull:
        with tqdm(total=1, desc="Installation des packages", ncols=80) as pbar:
            subprocess.run(
                ["pip", "install", "--user", "-r", "requirements.txt"],
                stdout=fnull,
                stderr=fnull,
                check=True
            )
            pbar.update(1)


def start_webservice():
    """
    Lance le webservice en arrière-plan.
    Processus démarré dans le répertoire 'src/webservice'.
    """
    print(f"{Fore.RED}=========== Démarrage du webservice ============\n")
    webservice_process = subprocess.Popen(
        ["python", "main_api.py"],
        cwd="src/webservice",
        stdout=subprocess.DEVNULL,  # Cache les logs du webservice
        stderr=subprocess.DEVNULL
    )
    time.sleep(1)  # Pause courte pour s'assurer que le processus démarre
    if webservice_process.poll() is None:
        print(f"{Fore.GREEN}✅ Webservice démarré avec succès.")
    else:
        print(f"{Fore.RED}❌ Échec du démarrage du webservice.")
    return webservice_process


def start_interface():
    """
    Lance l'interface utilisateur dans le terminal.
    Processus démarré dans le répertoire 'src/interface'.
    """
    print(f"{Fore.RED}========= Démarrage de l'interface utilisateur =========\n")
    subprocess.run(
        ["python", "main_interface.py"],
        cwd="src/interface",
    )


def clean_terminal():
    """
    Nettoie le terminal une fois l'application fermée.
    """
    print(f"{Fore.RED}=========== Nettoyage du terminal ============\n")
    os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    try:
        # Étape 1 : Mise à jour de pip
        update_pip()

        # Étape 2 : Installation des dépendances
        install_dependencies()

        # Étape 3 : Lancement du webservice
        webservice_process = start_webservice()

        # Étape 4 : Lancement de l'interface
        start_interface()

    finally:
        # Étape 5 : Arrêt du webservice et nettoyage du terminal
        print(f"{Fore.RED}=========== Arrêt du webservice ============\n")
        webservice_process.terminate()
        clean_terminal()

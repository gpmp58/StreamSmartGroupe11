import os
import subprocess
import time
from colorama import Fore, init

# Initialisation de colorama (nécessaire pour Windows)
init(autoreset=True)


def update_pip():
    """
    Met à jour `pip` à la dernière version disponible.
    """
    print(f"{Fore.RED}=========== Mise à jour de pip ============\n")
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip"], check=True)


def install_dependencies():
    """
    Installe les dépendances nécessaires pour le projet
    à partir du fichier requirements.txt en utilisant l'option --user.
    """
    print(f"{Fore.RED}=========== Installation des dépendances ============\n")
    subprocess.run(["pip", "install", "--user", "-r", "requirements.txt"], check=True)
<<<<<<< HEAD:start_application.py
=======
    loading_bar("Installation des dépendances en cours...")
>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb:src/start_application.py


def start_webservice():
    """
    Lance le webservice en arrière-plan.
    Processus démarré dans le répertoire 'src/webservice'.
    """
    print(f"{Fore.RED}=========== Démarrage du webservice ============\n")
    webservice_process = subprocess.Popen(
        ["python", "main_api.py"],
        cwd="src/webservice",
    )
    time.sleep(1)  # Pause courte pour s'assurer que le processus démarre correctement
    if webservice_process.poll() is None:
        print(f"{Fore.GREEN}✅ Webservice démarré avec succès.")
    else:
        print(f"{Fore.RED}❌ Échec du démarrage du webservice.")
    return webservice_process


def start_interface():
    """
    Lance l'interface utilisateur dans le terminal.
    Processus démarré dans le répertoire 'src/interface'.
    La fonction ne termine qu'à la fermeture de l'interface.
    """
    print(f"{Fore.RED}=========== Démarrage de l'interface utilisateur ============\n")
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


<<<<<<< HEAD:start_application.py
=======
def loading_bar(message):
    """
    Affiche une barre de progression pour une étape donnée.
    """
    print(f"{Fore.RED}{message}")
    for _ in tqdm(
        range(10), desc="Chargement", bar_format="{l_bar}{bar} | {n_fmt}/{total}"
    ):
        time.sleep(0.2)


>>>>>>> a73b05db2e8e2645eb8c912745b3cb85574b99eb:src/start_application.py
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

from InquirerPy import inquirer
from src.interface.session_manager import get_session_state
from src.interface.session_manager import clear_session_state
import os


# Fonction pour afficher les options du menu utilisateur
def main1():
    session_state = get_session_state()

    # Options disponibles selon l'état de connexion
    if not session_state["pseudo"]:
        print("Vous n'êtes pas connecté.")
        choix = inquirer.select(
            message="Choisissez une option :",
            choices=["Connexion", "Quitter"],
        ).execute()

        if choix == "Connexion":
            from src.interface.pages.interface_connexion import (
                connexion_utilisateur,
            )

            connexion_utilisateur()
        elif choix == "Quitter":
            print("Au revoir !")
            return
    else:
        choix = inquirer.select(
            message="Que souhaitez-vous faire ?",
            choices=[
                "Films",
                "Watchlist",
                "Recommendation de Watchlist",
                "Se déconnecter",
                "Quitter",
            ],
        ).execute()

        if choix == "Films":
            from src.interface.pages.interface_film import (
                page_recherche_films,
            )

            page_recherche_films()
        elif choix == "Watchlist":
            from src.interface.pages.interface_watchlist import (
                main_watchlist,
            )

            main_watchlist()
        elif choix == "Recommendation de Watchlist":
            from src.interface.pages.interface_recommandation import (
                main_recommandation,
            )

            main_recommandation()  # Interface de recommandation
        elif choix == "Se déconnecter":
            se_deconnecter()
        elif choix == "Quitter":
            print("Au revoir !")
            os.system("cls" if os.name == "nt" else "clear")
            exit()


# Fonction pour gérer la déconnexion
def se_deconnecter():
    """
    Gérer la déconnexion de l'utilisateur.
    """
    clear_session_state()
    main1()


# Lancement de l'application
if __name__ == "__main__":
    main1()

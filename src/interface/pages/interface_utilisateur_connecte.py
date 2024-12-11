from InquirerPy import inquirer
from src.interface.session_manager import get_session_state, clear_session_state
import os


def clear_terminal():
    """Nettoie le terminal."""
    os.system("cls" if os.name == "nt" else "clear")


# Fonction pour afficher les options du menu utilisateur
def main1():
    session_state = get_session_state()

    # Options disponibles selon l'état de connexion
    if not session_state.get("pseudo"):
        print("Vous n'êtes pas connecté.")
        choix = inquirer.select(
            message="Choisissez une option :",
            choices=["Connexion", "Quitter"],
        ).execute()

        if choix == "Connexion":
            from src.interface.pages.interface_connexion import connexion_utilisateur
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
                "Recommandation d'abonnement",
                "Se déconnecter",
                "Quitter",
            ],
        ).execute()

        if choix == "Films":
            from src.interface.pages.interface_film import page_recherche_films
            page_recherche_films()
        elif choix == "Watchlist":
            from src.interface.pages.interface_watchlist import main_watchlist
            main_watchlist()
        elif choix == "Recommandation d'abonnement":
            from src.interface.pages.interface_recommandation import main_recommandation
            main_recommandation()  # Interface de recommandation
        elif choix == "Se déconnecter":
            se_deconnecter()
        elif choix == "Quitter":
            print("Au revoir !")
            clear_terminal()
            exit()


# Fonction pour gérer la déconnexion
def se_deconnecter():
    """
    Gérer la déconnexion de l'utilisateur.
    """
    clear_session_state()
    clear_terminal()  # Nettoie le terminal avant de retourner au menu principal
    main1()


# Lancement de l'application
if __name__ == "__main__":
    main1()

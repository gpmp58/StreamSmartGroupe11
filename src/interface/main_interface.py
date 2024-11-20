from InquirerPy import prompt
 # Importer la fonction depuis le fichier correspondant

# Simulation d'un état de session
session_state = {"pseudo": None}

def main():
    """
    Page principale de l'application.
    """
    print("\n=== Application Multi-Page ===")
    afficher_etat_connexion()

    # Navigation en fonction de l'état de connexion
    if not session_state["pseudo"]:
        print("Vous n'êtes pas connecté.")
        choix = prompt(
            [
                {
                    "type": "list",
                    "name": "action",
                    "message": "Que souhaitez-vous faire ?",
                    "choices": [
                        {"name": "Connexion", "value": "connexion"},
                        {"name": "Création de Compte", "value": "creation"},
                        {"name": "Quitter", "value": "quitter"},
                    ],
                }
            ]
        )["action"]

        if choix == "connexion":
            from src.interface.pages.interface_connexion import connexion_utilisateur
            connexion_utilisateur()
        elif choix == "creation":
            from src.interface.pages.interface_creation_compte import page_creation_compte 
            page_creation_compte() 
        elif choix == "quitter":
            print("Merci d'avoir utilisé l'application. À bientôt !")
            return
    else:
        print(f"🎉 Vous êtes connecté en tant que {session_state['pseudo']}.")
        choix = prompt(
            [
                {
                    "type": "list",
                    "name": "action",
                    "message": "Que souhaitez-vous faire ?",
                    "choices": [
                        {"name": "Se Déconnecter", "value": "deconnexion"},
                        {"name": "Quitter", "value": "quitter"},
                    ],
                }
            ]
        )["action"]

        if choix == "deconnexion":
            se_deconnecter()
        elif choix == "quitter":
            print("Merci d'avoir utilisé l'application. À bientôt !")
            return


def interface_connexion():
    """
    Interface pour gérer la connexion utilisateur.
    """
    pseudo = prompt(
        [
            {
                "type": "input",
                "name": "pseudo",
                "message": "Entrez votre pseudo :",
                "validate": lambda text: len(text.strip()) > 0 or "Le pseudo ne peut pas être vide.",
            }
        ]
    )["pseudo"]

    session_state["pseudo"] = pseudo
    print(f"\n🎉 Connexion réussie ! Bienvenue, {pseudo}.")
    main()


def se_deconnecter():
    """
    Gérer la déconnexion de l'utilisateur.
    """
    print(f"\n👋 Déconnexion réussie. À bientôt, {session_state['pseudo']}!")
    session_state["pseudo"] = None
    main()


def afficher_etat_connexion():
    """
    Afficher l'état de connexion de l'utilisateur.
    """
    print("\n--- État de Connexion ---")
    if session_state["pseudo"]:
        print(f"Utilisateur : {session_state['pseudo']}")
        print("État : Connecté")
    else:
        print("Utilisateur : Non connecté")
        print("État : Déconnecté")
    print("-------------------------\n")


if __name__ == "__main__":
    main()

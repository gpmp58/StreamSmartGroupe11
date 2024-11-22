from InquirerPy import prompt
import requests
from src.interface.main_interface import main  # Retour au menu principal
from src.interface.session_manager import (
    set_session_state,
)  # Gestion de session globale

# URL de base de l'API FastAPI
LIEN_API = "http://127.0.0.1:8000"


# Fonction principale pour la création de compte
def page_creation_compte():
    print("=== Création de Compte Utilisateur ===")

    # Prompts pour recueillir les informations utilisateur
    questions = [
        {
            "type": "input",
            "name": "nom",
            "message": "Nom :",
            "validate": lambda result: len(result) > 0
            or "Le champ 'Nom' est obligatoire.",
        },
        {
            "type": "input",
            "name": "prenom",
            "message": "Prénom :",
            "validate": lambda result: len(result) > 0
            or "Le champ 'Prénom' est obligatoire.",
        },
        {
            "type": "input",
            "name": "pseudo",
            "message": "Pseudo :",
            "validate": lambda result: len(result) > 0
            or "Le champ 'Pseudo' est obligatoire.",
        },
        {
            "type": "input",
            "name": "adresse_mail",
            "message": "Adresse Mail :",
            "validate": lambda result: len(result) > 0
            or "Le champ 'Adresse Mail' est obligatoire.",
        },
        {
            "type": "password",
            "name": "mdp",
            "message": "Mot de Passe :",
            "validate": lambda result: len(result) > 0
            or "Le champ 'Mot de Passe' est obligatoire.",
        },
        {
            "type": "list",
            "name": "langue",
            "message": "Langue :",
            "choices": ["français", "anglais", "espagnol"],
        },
    ]

    # Récupérer les réponses de l'utilisateur
    answers = prompt(questions)

    # Préparer les données à envoyer à l'API
    data = {
        "nom": answers["nom"],
        "prenom": answers["prenom"],
        "pseudo": answers["pseudo"],
        "adresse_mail": answers["adresse_mail"],
        "mdp": answers["mdp"],
        "langue": answers["langue"],
    }

    # Effectuer l'appel API pour créer un compte
    try:
        response = requests.post(f"{LIEN_API}/utilisateurs", json=data)
        if response.status_code == 200:
            print(f"✅ Compte créé avec succès pour {answers['pseudo']}.")
            # Mettre à jour l'état de session avec le pseudo
            set_session_state(pseudo=answers["pseudo"], id_utilisateur=None)
        else:
            response_json = response.json()
            print(
                f"❌ Erreur : {response_json.get('detail', 'Erreur inconnue')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion à l'API : {e}")

    # Retourner au menu principal
    print("\nRedirection vers le menu principal...")
    main()


# Lancer le programme
if __name__ == "__main__":
    page_creation_compte()

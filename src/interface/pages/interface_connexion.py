from InquirerPy import prompt
import requests
from src.interface.main_interface import main
from src.interface.pages.interface_utilisateur_connecte import main1
from src.interface.session_manager import set_session_state, get_session_state  

# URL de base de l'API FastAPI
LIEN_API = "http://127.0.0.1:8000"

def connexion_utilisateur():
    """Connexion de l'utilisateur avec InquirerPy."""
    questions = [
        {
            "type": "input",
            "name": "pseudo",
            "message": "Entrez votre pseudo :",
        },
        {
            "type": "password",
            "name": "mdp",
            "message": "Entrez votre mot de passe :",
        },
    ]

    answers = prompt(questions)
    pseudo = answers.get("pseudo")
    mdp = answers.get("mdp")

    if not (pseudo and mdp):
        print("\n❌ Veuillez entrer votre pseudo et mot de passe.\n")
        return

    data = {"pseudo": pseudo, "mdp": mdp}

    try:
        # Appeler l'API pour se connecter
        response = requests.post(f"{LIEN_API}/utilisateurs/login", json=data)

        if response.status_code == 200:
            # Récupérer l'ID utilisateur
            id_response = requests.post(f"{LIEN_API}/utilisateurs/id", json={"pseudo": pseudo})
            if id_response.status_code == 200:
                id_utilisateur = id_response.json().get("id_utilisateur")

                if id_utilisateur:
                    # Mettre à jour l'état global via session_manager
                    set_session_state(pseudo=pseudo, id_utilisateur=id_utilisateur)

                    # Afficher les détails utilisateur
                    utilisateur_response = requests.get(f"{LIEN_API}/utilisateurs/{id_utilisateur}/afficher")
                    if utilisateur_response.status_code == 200:
                        utilisateur_info = utilisateur_response.json()
                        print("\n✅ Connexion réussie. Bienvenue !\n")
                        print("=== Informations Utilisateur ===")
                        print(f"🔹 Pseudo : {pseudo}")
                        print(f"🔹 ID Utilisateur : {id_utilisateur}")
                        print(f"🔹 Nom complet : {utilisateur_info.get('nom')} {utilisateur_info.get('prenom')}")
                        print(f"🔹 Adresse mail : {utilisateur_info.get('adresse_mail')}")
                        print(f"🔹 Langue préférée : {utilisateur_info.get('langue')}")
                        print("==============================\n")
                    else:
                        print("\n❌ Impossible de récupérer les détails utilisateur.\n")
                else:
                    print("\n❌ Erreur : ID utilisateur non récupéré.\n")
            else:
                print(f"\n❌ Erreur : {id_response.json().get('detail', 'Erreur inconnue')}\n")
        else:
            print(f"\n❌ Erreur : {response.json().get('detail', 'Erreur inconnue')}\n")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Erreur de connexion à l'API : {e}\n")
    
    # Rediriger vers la page utilisateur connecté
    main1()

if __name__ == "__main__":
    connexion_utilisateur()

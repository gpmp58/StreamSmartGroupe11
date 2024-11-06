import streamlit as st
import requests

# Interface principale avec Streamlit pour la gestion des utilisateurs via API REST
def page_connexion():
    st.title("Accueil - Connexion et Création de Compte Utilisateur")

    # Sélectionner l'action souhaitée : Se connecter ou Créer un compte
    action = st.radio("Choisissez une action :", ("Se connecter", "Créer un compte"))

    # URL de base de l'API FastAPI
    LIEN_API = "http://127.0.0.1:8000" 

    if action == "Créer un compte":
        st.header("Création de Compte Utilisateur")

        # Champs d'entrée pour l'utilisateur
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        pseudo = st.text_input("Pseudo")
        adresse_mail = st.text_input("Adresse Mail")
        mdp = st.text_input("Mot de Passe", type="password")
        langue = st.selectbox("Langue", ["français", "anglais", "espagnol"])

        # Lorsque l'utilisateur clique sur "Créer un compte"
        if st.button("Créer un compte"):
            if not (nom and prenom and pseudo and adresse_mail and mdp):
                st.error("Veuillez remplir tous les champs obligatoires.")
            else:
                # Préparer les données à envoyer à l'API
                data = {
                    "nom": nom,
                    "prenom": prenom,
                    "pseudo": pseudo,
                    "adresse_mail": adresse_mail,
                    "mdp": mdp,
                    "langue": langue,
                }

                # Effectuer l'appel API pour créer un compte
                response = requests.post(f"{LIEN_API}/utilisateurs", json=data)

                # Vérifier le résultat
                if response.status_code == 200:
                    st.success(f"Compte créé avec succès pour {pseudo}.")
                else:
                    st.error(f"Erreur : {response.json().get('detail', 'Erreur inconnue')}")

    elif action == "Se connecter":
        st.header("Connexion Utilisateur")

        # Champs de connexion
        pseudo = st.text_input("Pseudo")
        mdp = st.text_input("Mot de Passe", type="password")

        if st.button("Se connecter"):
            if not (pseudo and mdp):
                st.error("Veuillez entrer votre pseudo et mot de passe.")
            else:
                # Préparer les données à envoyer à l'API
                data = {
                    "pseudo": pseudo,
                    "mdp": mdp,
                }

                # Effectuer l'appel API pour se connecter
                response = requests.post(f"{LIEN_API}/utilisateurs/login", json=data)

                # Vérifier le résultat
                if response.status_code == 200:
                    st.success(response.json().get('message'))
                else:
                    st.error(f"Erreur : {response.json().get('detail', 'Erreur inconnue')}")

# Fonction à appeler dans le fichier principal pour cette interface
def page():
    page_connexion()

if __name__ == "__main__":
    page()

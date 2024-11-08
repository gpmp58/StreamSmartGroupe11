import streamlit as st
import requests
import interface_film as film  # Importer l'interface pour les films

# Interface pour la connexion utilisateur
def page_connexion():
    st.title("Connexion Utilisateur")

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

            # URL de base de l'API FastAPI
            LIEN_API = "http://127.0.0.1:8000"

            # Effectuer l'appel API pour se connecter
            try:
                response = requests.post(f"{LIEN_API}/utilisateurs/login", json=data)
                """
                # debug
                st.write(f"Statut de la réponse: {response.status_code}")
                st.write(f"Contenu de la réponse: {response.text}")
                """

                # Vérifier le résultat
                try:
                    response_json = response.json()
                    if response.status_code == 200:
                        st.session_state['logged_in'] = True
                        st.session_state['user'] = pseudo
                        st.success(response_json.get('message'))
                        st.write("Connexion réussie. Redirection vers la recherche de films.")
                        st.rerun()  # Appeler directement la page de recherche de films
                    else:
                        st.session_state['logged_in'] = False
                        st.session_state['user'] = 'Inconnu Non connecté'
                        st.error(f"Erreur : {response_json.get('detail', 'Erreur inconnue')}")
                except ValueError:
                    st.error("Erreur : La réponse de l'API n'est pas au format JSON.")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API : {e}")

# Interface pour la création de compte utilisateur
def page_creation_compte():
    st.title("Création de Compte Utilisateur")

    # Champs d'entrée pour l'utilisateur
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    pseudo = st.text_input("Pseudo")
    adresse_mail = st.text_input("Adresse Mail")
    mdp = st.text_input("Mot de Passe", type="password")
    langue = st.selectbox("Langue", ["français", "anglais", "espagnol"])

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

            # URL de base de l'API FastAPI
            LIEN_API = "http://127.0.0.1:8000"

            # Effectuer l'appel API pour créer un compte
            try:
                response = requests.post(f"{LIEN_API}/utilisateurs", json=data)
                st.write(f"Statut de la réponse: {response.status_code}")
                st.write(f"Contenu de la réponse: {response.text}")
                
                try:
                    response_json = response.json()
                    if response.status_code == 200:
                        st.success(f"Compte créé avec succès pour {pseudo}.")
                    else:
                        st.error(f"Erreur : {response_json.get('detail', 'Erreur inconnue')}")
                except ValueError:
                    st.error("Erreur : La réponse de l'API n'est pas au format JSON.")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API : {e}")

# Fonction principale à appeler depuis main_interface.py
def page():
    page_connexion()

# Fonction principale pour la création de compte à appeler depuis main_interface.py
def page_creation_compte_wrapper():
    page_creation_compte()

if __name__ == "__main__":
    page()

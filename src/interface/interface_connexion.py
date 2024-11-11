import streamlit as st
import requests

# URL de base de l'API FastAPI
LIEN_API = "http://127.0.0.1:8000"

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

            # Effectuer l'appel API pour se connecter
            try:
                response = requests.post(f"{LIEN_API}/utilisateurs/login", json=data)

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

# Fonction principale pour la connexion
def page():
    page_connexion()

if __name__ == "__main__":
    page()

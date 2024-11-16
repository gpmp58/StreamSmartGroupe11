import streamlit as st
import requests
from src.interface.main_interface import afficher_etat_connexion

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
                if response.status_code == 200:
                    # Récupérer l'ID utilisateur depuis la route /utilisateurs/id
                    try:
                        id_response = requests.post(f"{LIEN_API}/utilisateurs/id", json={"pseudo": pseudo})
                        if id_response.status_code == 200:
                            id_utilisateur = id_response.json().get('id_utilisateur')

                            # Vérifier si l'ID utilisateur est valide
                            if id_utilisateur:
                                # Stocker les informations utilisateur dans la session
                                st.session_state['pseudo'] = pseudo
                                st.session_state['id_utilisateur'] = id_utilisateur

                                # Faire une requête pour récupérer les détails utilisateur
                                try:
                                    utilisateur_response = requests.get(f"{LIEN_API}/utilisateurs/{id_utilisateur}/afficher")
                                    if utilisateur_response.status_code == 200:
                                        utilisateur_info = utilisateur_response.json()

                                        # Afficher les informations utilisateur
                                        st.success(f"Connexion réussie. Bienvenue, {pseudo}.")
                                        st.write(f"Votre identifiant utilisateur est : {id_utilisateur}.")
                                        st.write(f"**Nom complet :** {utilisateur_info.get('nom')} {utilisateur_info.get('prenom')}")
                                        st.write(f"**Pseudo :** {utilisateur_info.get('pseudo')}")
                                        st.write(f"**Adresse mail :** {utilisateur_info.get('adresse_mail')}")
                                        st.write(f"**Langue :** {utilisateur_info.get('langue')}")

                                        # Mise à jour de la sidebar
                                        with st.sidebar:
                                            st.success(f"🎉 Connecté avec succès !")
                                            st.write(f"**Pseudo :** {st.session_state['pseudo']}")
                                            st.write(f"**ID Utilisateur :** {st.session_state['id_utilisateur']}")
                                            st.write(f"**Nom complet :** {utilisateur_info.get('nom')} {utilisateur_info.get('prenom')}")
                                            st.write(f"**Pseudo :** {utilisateur_info.get('pseudo')}")
                                            st.write(f"**Adresse mail :** {utilisateur_info.get('adresse_mail')}")
                                            st.write(f"**Langue :** {utilisateur_info.get('langue')}")
                                            st.switch_page("pages/interface_utilisateur_connecte.py")
                                    else:
                                        st.error("Impossible de récupérer les détails utilisateur.")
                                except requests.exceptions.RequestException as e:
                                    st.error(f"Erreur lors de la récupération des informations utilisateur : {e}")
                            else:
                                st.error("Erreur : ID utilisateur non récupéré.")
                        else:
                            st.error(f"Erreur : {id_response.json().get('detail', 'Erreur inconnue')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Erreur lors de la récupération de l'ID utilisateur : {e}")
                else:
                    st.error(f"Erreur : {response.json().get('detail', 'Erreur inconnue')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API : {e}")

# Fonction principale pour la connexion
def page():
    page_connexion()

# Lancer la page
if __name__ == "__main__":
    page()

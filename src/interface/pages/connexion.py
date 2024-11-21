import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"  # URL de l'API

def afficher_connexion():
    st.subheader("Connexion")
    pseudo = st.text_input("Pseudo")
    mdp = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        try:
            # Envoi des informations de connexion à l'API
            response = requests.post(f"{BASE_URL}/utilisateurs/login", json={"pseudo": pseudo, "mdp": mdp})
            
            if response.status_code == 200:
                # Si la connexion réussie, stocke l'utilisateur dans session_state
                st.session_state["utilisateur_connecte"] = pseudo  # On stocke le pseudo
                st.session_state["id_utilisateur"] = response.json().get("id_utilisateur")  # ID utilisateur si disponible

                st.success("Connexion réussie !")
                st.write("Message de l'API :", response.json().get("message"))
                
                # Redirection vers la page des watchlists ou autre page appropriée
                st.rerun()  # Cela recharge l'application et applique la redirection
            else:
                st.error("Erreur : " + response.json().get("detail", "Connexion échouée."))
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur lors de la connexion à l'API : {e}")

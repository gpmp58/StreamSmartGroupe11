import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

def afficher_creation_compte():
    st.subheader("Créer un compte")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    pseudo = st.text_input("Pseudo")
    adresse_mail = st.text_input("Adresse mail")
    mdp = st.text_input("Mot de passe", type="password")
    langue = st.selectbox("Langue", ["français", "anglais"])

    if st.button("Créer un compte"):
        try:
            response = requests.post(
                f"{BASE_URL}/utilisateurs",
                json={
                    "nom": nom,
                    "prenom": prenom,
                    "pseudo": pseudo,
                    "adresse_mail": adresse_mail,
                    "mdp": mdp,
                    "langue": langue,
                },
            )
            if response.status_code == 200:
                st.success("Compte créé avec succès !")
                st.write("Bienvenue :", response.json())
            else:
                st.error("Erreur : " + response.json().get("detail", "Création de compte échouée."))
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur lors de la connexion à l'API : {e}")

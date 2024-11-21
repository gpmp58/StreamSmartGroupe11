# main.py
import streamlit as st
from pages import connexion, creation_compte, rechercher_film, watchlist

# Menu latéral
menu = st.sidebar.selectbox(
    "Navigation",
    ["Connexion", "Créer un compte", "Recherche", "Watchlist", "Critères"]
)

# Vérification de la connexion de l'utilisateur
if "utilisateur_connecte" in st.session_state:
    # Si l'utilisateur est connecté, il peut voir et gérer ses watchlists
    if menu == "Watchlist":
        watchlist.afficher_watchlist()  # Affiche les watchlists de l'utilisateur connecté
    elif menu == "Critères":
        # Gérer les critères de recommandation
        pass
else:
    # Si l'utilisateur n'est pas connecté, on affiche la page de connexion ou de création de compte
    if menu == "Connexion":
        connexion.afficher_connexion()  # Affiche la page de connexion
    elif menu == "Créer un compte":
        # Créer un compte (à développer)
        pass
    else:
        st.warning("Veuillez vous connecter pour accéder à cette section.")

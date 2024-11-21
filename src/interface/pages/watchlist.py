import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"  # URL de l'API

def afficher_watchlist():
    st.subheader("Mes Watchlists")

    # Vérifier si l'utilisateur est connecté
    if "utilisateur_connecte" not in st.session_state:
        st.warning("Vous devez être connecté pour accéder à vos watchlists.")
        return

    # Récupérer les watchlists de l'utilisateur
    id_utilisateur = st.session_state.get("id_utilisateur")
    try:
        response = requests.get(f"{BASE_URL}/watchlists/{id_utilisateur}")
        if response.status_code == 200:
            watchlists = response.json()  # Supposons que l'API retourne une liste de watchlists

            if not watchlists:
                st.write("Vous n'avez pas encore de watchlist.")
            else:
                # Afficher les watchlists existantes
                for watchlist in watchlists:
                    st.write(f"**{watchlist['nom_watchlist']}**")
                    
                    # Option pour ajouter un film à cette watchlist
                    ajouter_film = st.button(f"Ajouter un film à {watchlist['nom_watchlist']}")
                    if ajouter_film:
                        # Demander à l'utilisateur de saisir le nom d'un film
                        film_nom = st.text_input("Nom du film à ajouter")
                        if st.button("Ajouter"):
                            # Logique pour ajouter le film à cette watchlist
                            ajouter_film_watchlist(watchlist['id_watchlist'], film_nom)
        else:
            st.error("Erreur lors du chargement de vos watchlists.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des watchlists : {e}")

def ajouter_film_watchlist(id_watchlist, film_nom):
    """Fonction pour ajouter un film à une watchlist"""
    if not film_nom:
        st.error("Veuillez entrer un nom de film.")
        return
    
    try:
        response = requests.post(
            f"{BASE_URL}/watchlists/{id_watchlist}/ajouter_film",
            json={"nom_film": film_nom}
        )
        if response.status_code == 200:
            st.success(f"Film '{film_nom}' ajouté à la watchlist avec succès.")
        else:
            st.error(f"Erreur : {response.json().get('detail', 'Erreur inconnue')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'ajout du film : {e}")
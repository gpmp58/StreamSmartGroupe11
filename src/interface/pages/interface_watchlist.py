import streamlit as st
import requests
from src.interface.main_interface import afficher_etat_connexion

# Configuration de la page principale
st.set_page_config(page_title="Gestion des Watchlists", layout="wide")

# Initialisation de l'état de session pour l'utilisateur
if 'pseudo' not in st.session_state:
    st.session_state['pseudo'] = None

# URL de base de l'API
LIEN_API = "http://127.0.0.1:8000"

# Vérifier si l'utilisateur est connecté
if st.session_state['pseudo']:
    # Afficher les informations de l'utilisateur dans la barre latérale
    with st.sidebar:
        st.write(f"**Utilisateur :** {st.session_state['pseudo']}")
        st.write("**État : Connecté**")
        if st.button("Se déconnecter"):
            st.session_state['pseudo'] = None
            st.rerun()

    # Menu principal pour la gestion des watchlists
    st.title("🎬 Gestion des Watchlists")
    option = st.selectbox(
        "Choisissez une fonctionnalité",
        [
            "Créer une Watchlist",
            "Supprimer une Watchlist",
            "Ajouter un Film à une Watchlist",
            "Supprimer un Film d'une Watchlist",
            "Récupérer les Films d'une Watchlist",
            "Afficher les Watchlists"
        ]
    )

    afficher_etat_connexion()

    # Fonction pour créer une nouvelle watchlist
    def creer_watchlist():
        st.subheader("➕ Créer une Nouvelle Watchlist")
        nom_watchlist = st.text_input("Nom de la watchlist", placeholder="Nom de la watchlist")
        if st.button("Créer"):
            if not nom_watchlist.strip():
                st.warning("Veuillez entrer un nom de watchlist.")
                return

            data = {"nom_watchlist": nom_watchlist, "id_utilisateur": st.session_state["pseudo"]}
            try:
                response = requests.post(f"{LIEN_API}/watchlists", json=data)
                if response.status_code == 200:
                    st.success("✅ Watchlist créée avec succès !")
                else:
                    st.error(f"Erreur : {response.json().get('detail', 'ERREUR INCONUE')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API : {e}")

    # Fonction pour afficher les watchlists
    def afficher_watchlist_utilisateur():
        st.subheader("📂 Afficher les Watchlists")
        try:
            response = requests.get(f"{LIEN_API}/watchlists/utilisateur/{st.session_state['pseudo']}")
            if response.status_code == 200:
                watchlists = response.json().get("watchlists", [])
                if watchlists:
                    for watchlist in watchlists:
                        st.markdown(f"""
                        <div style="border: 1px solid #444; border-radius: 8px; padding: 10px; margin-bottom: 10px;">
                            <h3>📋 {watchlist['nom_watchlist']} (ID : {watchlist['id_watchlist']})</h3>
                            <p><strong>Films :</strong></p>
                            <ul>
                            {''.join(f"<li>{film['nom_film']} (ID : {film['id_film']})</li>" for film in watchlist.get('films', []))}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Aucune watchlist trouvée pour cet utilisateur.")
            else:
                st.error(f"Erreur : {response.json().get('detail', 'Erreur lors de la récupération des watchlists.')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion à l'API : {e}")

    # Fonction pour ajouter un film à une watchlist
    def ajouter_film():
        st.subheader("🎥 Ajouter un Film à une Watchlist")
        numero_watchlist = st.number_input("Numéro de la watchlist", min_value=1, step=1)
        numero_film = st.number_input("Numéro du film", min_value=1, step=1)
        if st.button("Ajouter"):
            if not numero_watchlist or not numero_film:
                st.warning("Veuillez remplir tous les champs avant de valider.")
                return

            data = {"id_watchlist": numero_watchlist, "id_film": numero_film}
            try:
                response = requests.post(f"{LIEN_API}/watchlists/ajouter_film", json=data)
                if response.status_code == 200:
                    st.success("✅ Film ajouté à la watchlist avec succès !")
                else:
                    st.error(f"Erreur : {response.json().get('detail', 'ERREUR INCONNUE')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API : {e}")

    # Fonction pour supprimer une watchlist
    def supprimer_watchlist():
        st.subheader("🗑️ Supprimer une Watchlist")
        numero_watchlist = st.number_input("Numéro de la watchlist", min_value=1, step=1)
        if st.button("Supprimer"):
            try:
                response = requests.delete(f"{LIEN_API}/watchlists/{numero_watchlist}")
                if response.status_code == 200:
                    st.success("🗑️ Watchlist supprimée avec succès.")
                else:
                    st.error(f"Erreur : {response.json().get('detail', 'Erreur lors de la suppression.')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API : {e}")

    # Fonction pour supprimer un film d'une watchlist
    def supprimer_film():
        st.subheader("🗑️ Supprimer un Film d'une Watchlist")
        numero_watchlist = st.number_input("Numéro de la watchlist", min_value=1, step=1)
        numero_film = st.number_input("Numéro du film", min_value=1, step=1)
        if st.button("Supprimer"):
            try:
                response = requests.delete(f"{LIEN_API}/watchlists/{numero_watchlist}/supprimer_film/{numero_film}")
                if response.status_code == 200:
                    st.success("✅ Film supprimé avec succès.")
                else:
                    st.error(f"Erreur : {response.json().get('detail', 'Erreur lors de la suppression du film.')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API : {e}")

    # Fonction pour récupérer les films d'une watchlist
    def recuperer_films_watchlist():
        st.subheader("📄 Récupérer les Films d'une Watchlist")
        numero_watchlist = st.number_input("Numéro de la watchlist", min_value=1, step=1)
        if st.button("Récupérer"):
            try:
                response = requests.get(f"{LIEN_API}/watchlists/{numero_watchlist}/films")
                if response.status_code == 200:
                    films = response.json().get("films", [])
                    if films:
                        st.table([{"ID Film": film["id_film"], "Nom Film": film["nom_film"]} for film in films])
                    else:
                        st.warning("Aucun film trouvé dans cette watchlist.")
                else:
                    st.error(f"Erreur : {response.json().get('detail', 'Erreur lors de la récupération des films.')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API : {e}")

    # Afficher la fonctionnalité choisie
    if option == "Créer une Watchlist":
        creer_watchlist()
    elif option == "Afficher les Watchlists":
        afficher_watchlist_utilisateur()
    elif option == "Ajouter un Film à une Watchlist":
        ajouter_film()
    elif option == "Supprimer une Watchlist":
        supprimer_watchlist()
    elif option == "Supprimer un Film d'une Watchlist":
        supprimer_film()
    elif option == "Récupérer les Films d'une Watchlist":
        recuperer_films_watchlist()
else:
    st.warning("Veuillez vous connecter pour accéder à vos watchlists.")

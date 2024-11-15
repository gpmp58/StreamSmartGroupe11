import streamlit as st
import requests
from src.main_interface import afficher_etat_connexion

# URL de base de l'API
LIEN_API = "http://127.0.0.1:8000"

# Titre principal de l'application
st.title("🎬 Gestion de vos Watchlists 🎬")

# Menu déroulant pour sélectionner la fonctionnalité
option = st.selectbox(
    "Choisissez une fonctionnalité",
    [
        "Créer une Watchlist",
        "Supprimer une Watchlist",
        "Ajouter un Film à une Watchlist",
        "Supprimer un Film d'une Watchlist",
        "Récupérer les Films d'une Watchlist",
        "Afficher les Watchlists d'un Utilisateur"
    ]
)

afficher_etat_connexion()

# Fonction pour créer une nouvelle watchlist
def creer_watchlist():
    st.subheader("➕ Créer une Nouvelle Watchlist")
    nom_watchlist = st.text_input("Nom de la watchlist", placeholder="Nom de la watchlist")
    numero_utilisateur = st.number_input("Numéro utilisateur", min_value=1, step=1)
    if st.button("Créer"):
        if nom_watchlist and numero_utilisateur:
            data = {"nom_watchlist": nom_watchlist, "id_utilisateur": numero_utilisateur}
            try:
                response = requests.post(f"{LIEN_API}/watchlists", json=data)
                if response.status_code == 200:
                    st.success("✅ Watchlist créée avec succès !")
                else:
                    st.error(response.json().get("detail", "Erreur inconnue lors de la création."))
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API : {e}")

# Fonction pour afficher toutes les watchlists d'un utilisateur
def afficher_watchlist_utilisateur():
    st.subheader("📂 Afficher les Watchlists d'un Utilisateur")
    id_utilisateur = st.number_input("Numéro utilisateur", min_value=1, step=1)
    if st.button("Afficher les Watchlists"):
        try:
            # Requête pour récupérer les watchlists de l'utilisateur
            response = requests.get(f"{LIEN_API}/watchlists/utilisateur/{id_utilisateur}")
            if response.status_code == 200:
                watchlists = response.json().get("watchlists", [])
                if watchlists:
                    for watchlist in watchlists:
                        st.write(f"**Watchlist :** {watchlist['nom_watchlist']} (ID : {watchlist['id_watchlist']})")
                        films = watchlist.get("films", [])
                        if films:
                            st.write("Films dans cette watchlist :")
                            for film in films:
                                st.write(f"- {film['nom_film']} (ID : {film['id_film']})")
                        else:
                            st.write("Aucun film dans cette watchlist.")
                        st.write("---")  # Séparateur entre les watchlists
                else:
                    st.warning("Cet utilisateur n'a pas de watchlists.")
            else:
                st.error(response.json().get("detail", "Erreur lors de la récupération des watchlists."))
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
                st.error(response.json().get("detail", "Erreur lors de la suppression de la watchlist."))
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion à l'API : {e}")

# Fonction pour ajouter un film à une watchlist
def ajouter_film():
    st.subheader("🎥 Ajouter un Film à une Watchlist")
    numero_watchlist_ajout = st.number_input("Numéro de la watchlist", min_value=1, step=1)
    numero_film = st.number_input("Numéro du film", min_value=1, step=1)
    nom_film = st.text_input("Nom du film", placeholder="Nom du film")
    if st.button("Ajouter"):
        if numero_watchlist_ajout and numero_film and nom_film:
            data = {"id_watchlist": numero_watchlist_ajout, "id_film": numero_film, "nom_film": nom_film}
            try:
                response = requests.post(f"{LIEN_API}/watchlists/ajouter_film", json=data)
                if response.status_code == 200:
                    st.success("✅ Film ajouté à la watchlist avec succès !")
                else:
                    st.error(response.json().get("detail", "Erreur lors de l'ajout du film."))
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API : {e}")

# Fonction pour supprimer un film d'une watchlist
def supprimer_film():
    st.subheader("🗑️ Supprimer un Film d'une Watchlist")
    numero_watchlist_suppression = st.number_input("Numéro de la watchlist", min_value=1, step=1)
    numero_film_suppression = st.number_input("Numéro du film", min_value=1, step=1)
    if st.button("Supprimer"):
        try:
            response = requests.delete(f"{LIEN_API}/watchlists/{numero_watchlist_suppression}/supprimer_film/{numero_film_suppression}")
            if response.status_code == 200:
                st.success("✅ Film supprimé de la watchlist avec succès.")
            else:
                st.error(response.json().get("detail", "Erreur lors de la suppression du film."))
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion à l'API : {e}")

# Fonction pour récupérer les films d'une watchlist (sans affichage détaillé)
def recuperer_films_watchlist():
    st.subheader("📄 Récupérer les Films d'une Watchlist")
    numero_watchlist_recuperation = st.number_input("Numéro de la watchlist", min_value=1, step=1)
    if st.button("Récupérer"):
        try:
            response = requests.get(f"{LIEN_API}/watchlists/{numero_watchlist_recuperation}/films")
            if response.status_code == 200:
                st.success("✅ Films récupérés avec succès (détails non affichés ici).")
            else:
                st.error(response.json().get("detail", "Erreur lors de la récupération des films."))
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion à l'API : {e}")

# Afficher la fonctionnalité choisie
if option == "Créer une Watchlist":
    creer_watchlist()
elif option == "Supprimer une Watchlist":
    supprimer_watchlist()
elif option == "Ajouter un Film à une Watchlist":
    ajouter_film()
elif option == "Supprimer un Film d'une Watchlist":
    supprimer_film()
elif option == "Récupérer les Films d'une Watchlist":
    recuperer_films_watchlist()
elif option == "Afficher les Watchlists d'un Utilisateur":
    afficher_watchlist_utilisateur()

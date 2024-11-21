import streamlit as st
import requests
from src.webservice.business_object.film import Film  # Importer la classe Film

# URL de l'API FastAPI
BASE_URL = "http://127.0.0.1:8000"  # Change si nécessaire

def afficher_recherche():
    st.title("Recherche de Film")

    # Entrée pour rechercher un film
    nom_film = st.text_input("Nom du film")

    if st.button("Rechercher"):
        if nom_film:
            try:
                # Envoi de la requête à l'API FastAPI pour rechercher le film
                response = requests.post(f"{BASE_URL}/films/recherche", json={"nom_film": nom_film})

                if response.status_code == 200:
                    films_trouves = response.json().get("films")
                    if films_trouves:
                        st.write("Films trouvés :")

                        # Utilisation de st.columns pour afficher les films côte à côte
                        cols = st.columns(3)  # Modifier le nombre de colonnes selon tes besoins (ici 3 films par ligne)
                        
                        col_idx = 0
                        for id_film, film in films_trouves.items():
                            # Créer un objet Film pour récupérer l'image
                            film_obj = Film(id_film)

                            # Affichage des films côte à côte dans les colonnes
                            with cols[col_idx]:
                                st.subheader(film)  # Affichage du nom du film
                                st.image(film_obj.image, width=200)  # Affichage de l'image du film

                                # Bouton pour voir les détails du film dans un expander
                                with st.expander(f"Détails de {film}"):
                                    st.subheader("Description")
                                    st.write(film_obj.details["description"])

                                    st.subheader("Date de sortie")
                                    st.write(film_obj.details["date_sortie"])

                                    st.subheader("Genres")
                                    st.write(", ".join(film_obj.details["genres"]))

                                    st.subheader("Durée")
                                    st.write(film_obj.details["duree"])

                            # Changer de colonne après chaque film
                            col_idx += 1
                            if col_idx == 3:  # Si nous avons atteint 3 films par ligne, repartir à la première colonne
                                col_idx = 0
                    else:
                        st.warning("Aucun film trouvé.")
                else:
                    st.error("Erreur de recherche.")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur lors de la requête : {e}")
        else:
            st.warning("Veuillez entrer un nom de film.")

# Afficher la recherche
afficher_recherche()

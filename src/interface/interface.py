import streamlit as st
from src.webservice.services.service_film import FilmService
from src.webservice.business_object.film import Film

# Fonction pour rechercher les films et afficher les résultats
def rechercher_films(nom_film):
    try:
        film_service = FilmService(nom_film)
        films = film_service.rechercher_film()

        if films:
            cols = st.columns(3)  # Créez trois colonnes

            for i, (film_id, film_name) in enumerate(films.items()):
                film = Film(film_id)
                with cols[i % 3]:  # Utilise les colonnes en boucle
                    if film.image:
                        # Affichage de l'image avec une largeur de 200 pixels
                        st.image(film.image, caption=film_name, use_column_width=False, width=200)
                        st.write(film_name)  # Affichage du nom du film
                    else:
                        st.write("Image non disponible")
        else:
            st.write("Aucun film trouvé avec ce nom.")
    except Exception as e:
        st.error(str(e))  # Affiche seulement le message d'erreur

# Interface principale avec Streamlit
def main():
    st.title("Recherche de films")
    nom_film = st.text_input("Entrez le nom du film :")
    if st.button("Rechercher"):
        rechercher_films(nom_film)

if __name__ == "__main__":
    main()

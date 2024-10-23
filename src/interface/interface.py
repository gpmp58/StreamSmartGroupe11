import streamlit as st
from src.webservice.services.service_film import FilmService
from src.webservice.business_object.film import Film

# Fonction pour rechercher les films et afficher les résultats
def rechercher_films(nom_film):
    try:
        film_service = FilmService(nom_film)
        films = film_service.rechercher_film()

        if films:
            # Compte le nombre total de films
            film_items = list(films.items())

            for i in range(0, len(film_items), 4):  # Parcourir les films par groupes de 4
                cols = st.columns(4)  # Créer 4 colonnes pour chaque ligne

                # Afficher 4 films par ligne
                for j, (film_id, film_name) in enumerate(film_items[i:i+4]):
                    film = Film(film_id)
                    with cols[j]:  # Utiliser les colonnes en boucle
                        if film.image:
                            # HTML et CSS pour un design moderne avec effet de survol
                            st.markdown(f"""
                                <div style="border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
                                            text-align: center; margin: 10px; background-color: #f8f8f8; width: 220px; height: 350px;">
                                    <img src="{film.image}" alt="{film_name}" style="width: 100%; height: auto; max-height: 200px;
                                        transition: transform 0.3s ease, filter 0.3s ease; object-fit: cover;"/>
                                    <div style="padding: 10px; font-weight: bold; font-size: 16px; color: #333;">
                                        {film_name}
                                    </div>
                                </div>
                                <style>
                                    div:hover img {{
                                        transform: translateY(-10px);
                                        filter: brightness(1.1);
                                    }}
                                </style>
                            """, unsafe_allow_html=True)
                        else:
                            st.write("Image non disponible")

                # Réduire l'espace blanc entre les lignes
                st.markdown("<hr style='border: 0; height: 1px; background-color: #f0f0f0; margin: 5px 0;'>", unsafe_allow_html=True)

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

import streamlit as st
from src.webservice.services.service_film import FilmService
from src.webservice.business_object.film import Film

# Fonction pour tronquer le texte
def tronquer_texte(texte, max_longueur):
    if len(texte) > max_longueur:
        return texte[:max_longueur] + "..."
    return texte

# Fonction pour rechercher les films et afficher les résultats
def rechercher_films(nom_film):
    try:
        film_service = FilmService(nom_film)
        films = film_service.rechercher_film()

        if films:
            film_items = list(films.items())

            for i in range(0, len(film_items), 4):
                cols = st.columns(4)

                for j, (film_id, film_name) in enumerate(film_items[i:i+4]):
                    film = Film(film_id)
                    with cols[j]:
                        description = film.details.get("description", "Pas de description disponible.")
                        description_tronquee = tronquer_texte(description, 300)

                        st.markdown(f"""
                            <a href="/?film_id={film_id}" target="_self" style="text-decoration: none;">
                                <div class="film-card">
                                    {f'<img src="{film.image}" alt="{film_name}"/>' if film.image else ''}
                                    <div class="film-info">
                                        {description_tronquee}
                                    </div>
                                    <div style="padding: 5px 0; font-weight: bold; font-size: 14px; color: #ffffff; text-align: center;">
                                        {film_name}
                                    </div>
                                </div>
                            </a>
                        """, unsafe_allow_html=True)

                st.markdown("<hr style='border: 0; height: 1px; background-color: #444; margin: 5px 0;'>", unsafe_allow_html=True)

        else:
            st.write("Aucun film trouvé avec ce nom.")
    except Exception as e:
        st.error(str(e))

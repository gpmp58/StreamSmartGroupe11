import streamlit as st
from src.webservice.business_object.film import Film

def afficher_details_film(film_id):
    film = Film(film_id)  # Récupérer les détails du film
    st.title(film.details.get("name", "Titre non disponible"))

    # Conteneur pour l'image et les informations
    details_container = st.container()
    with details_container:
        col1, col2 = st.columns([1, 2])
        with col1:
            if film.image:
                st.image(film.image, use_container_width=False, width=250)
            else:
                st.write("Image non disponible.")

        with col2:
            st.markdown(f"<div class='details-title'>{film.details.get('name', 'Titre non disponible')}</div>", unsafe_allow_html=True)

            # Section pour la description
            st.markdown("<div class='details-section'>", unsafe_allow_html=True)
            description = film.details.get('description')
            if len(description) > 0:
                st.markdown(f"<div class='details-description'>{description}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='details-description'>Pas de description disponible.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Informations sur le film
            st.markdown("<div class='details-section'>", unsafe_allow_html=True)
            st.markdown(f"<div class='details-info'>Date de sortie : {film.details.get('date_sortie', 'Date non disponible')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='details-info'>Durée : {film.details.get('duree', 'Durée non disponible')} </div>", unsafe_allow_html=True)
            st.markdown(f"<div class='details-info'>Genres : {', '.join(film.details.get('genres', ['Pas de genres disponibles']))}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Recherche des sites de streaming
            streaming_sites = film.streaming
            if not streaming_sites:
                st.write("Pas de plateformes de streaming disponibles.")
            else:
                st.markdown("<div class='streaming-links'>Disponibles sur :</div>", unsafe_allow_html=True)

                st.markdown("<div style='display: flex; flex-wrap: wrap; margin-top: 10px;'>", unsafe_allow_html=True)
                for site in streaming_sites:
                    if "logo" in site:
                        st.markdown(f"""
                            <div style='margin-right: 10px;'>
                                <a href='{site["id"]}' target='_blank'>
                                    <img src='https://image.tmdb.org/t/p/w45{site["logo"]}' alt='{site["name"]}' style='width: 30px; height: auto; border-radius: 5px;' />
                                </a>
                            </div>
                        """, unsafe_allow_html=True)

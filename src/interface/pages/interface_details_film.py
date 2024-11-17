import streamlit as st
from src.webservice.business_object.film import Film
import requests
from src.interface.main_interface import afficher_etat_connexion

# Injecter le CSS global
def inject_css2():
    st.markdown("""
    <style>
    /* Couleurs et styles globaux */
    .reportview-container {
        background-color: #1e1e1e;
    }
    .sidebar .sidebar-content {
        background-color: #2e2e2e;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
    p, li {
        color: #cccccc;
    }

    /* Styles des cartes de films */
    .film-card {
        position: relative;
        overflow: hidden;
        margin: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(255, 255, 255, 0.3);
        background-color: #2e2e2e;
        width: 160px;
        height: 270px;
        margin-right: 20px;
        margin-left: 20px;
    }
    .film-card img {
        width: 100%;
        height: auto;
        object-fit: cover;
        transition: filter 0.3s ease;
    }
    .film-card:hover img {
        filter: brightness(50%);
    }
    .film-info {
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        transform: translateY(-50%);
        padding: 5px;
        font-weight: bold;
        font-size: 12px;
        color: #ffffff;
        background-color: rgba(0, 0, 0, 0.5);
        text-align: center;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .film-card:hover .film-info {
        opacity: 1;
    }

    /* Détails du film */
    .details-container {
        display: flex;
        align-items: flex-start;
        margin: 20px;
        background-color: #2e2e2e;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(255, 255, 255, 0.2);
    }
    .details-image {
        background-color: #FFDD57;
        padding: 10px;
        border-radius: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 350px;
        height: 450px;
        margin-right: 20px;
    }
    .details-title {
        font-size: 24px;
        font-weight: bold;
        color: #FFDD57;
        border-bottom: 2px solid #FFDD57;
        padding-bottom: 5px;
        margin-bottom: 10px;
    }
    .details-section {
        background-color: #3e3e3e;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .details-description, .details-info {
        font-size: 16px;
        color: #cccccc;
        margin: 5px 0;
    }

    /* Liens vers les plateformes de streaming */
    .streaming-links {
        margin-top: 10px;
        font-weight: bold;
        color: #FFDD57;
    }
    .streaming-links img {
        width: 30px;
        height: auto;
        border-radius: 5px;
        margin-right: 5px;
    }

    /* Bouton "Ajouter à la watchlist" */
    .watchlist-button {
        background-color: #FFDD57;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        text-align: center;
        width: 100%;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }
    .watchlist-button:hover {
        background-color: #ffcc00;
        transform: scale(1.05);
    }

    /* Grille de logos de streaming */
    .streaming-logo {
        border: 1px solid #444;
        padding: 10px;
        border-radius: 10px;
        background-color: #333;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 60px;
        width: 60px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialisation de l'état de session si nécessaire
if 'pseudo' not in st.session_state:
    st.session_state['pseudo'] = None
if 'id_utilisateur' not in st.session_state:
    st.session_state['id_utilisateur'] = None

query_params = st.query_params  # Utiliser la bonne méthode
if "film_id" in query_params:
    film_id = query_params["film_id"]
else:
    raise Exception("Pas d'id pour le film")
if "pseudo" in query_params:
    st.session_state['pseudo'] = query_params["pseudo"]
if "id_utilisateur" in query_params:
    st.session_state['id_utilisateur'] = query_params["id_utilisateur"]

# Barre latérale pour afficher les informations de l'utilisateur
with st.sidebar:
    if st.session_state['pseudo']:
        st.write(f"**Utilisateur :** {st.session_state['pseudo']}")
        st.write(f"**ID Utilisateur :** {st.session_state['id_utilisateur']}")
        st.write("**État : Connecté**")
    else:
        st.write("Utilisateur : Non connecté")
        st.write("État : Déconnecté")



print(f"afficher détail film pour le film {film_id}")
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

        # Bouton "Ajouter à la watchlist"
        st.markdown("""<button class="watchlist-button">Ajouter à la watchlist</button>""", unsafe_allow_html=True)

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

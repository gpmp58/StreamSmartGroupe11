import streamlit as st
from interface_recherche_film import rechercher_films
from interface_details_film import afficher_details_film

# Injecter le CSS global
def inject_css():
    st.markdown("""
        <style>
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
            .film-card {
        position: relative;
        overflow: hidden;
        margin: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(255, 255, 255, 0.3);
        background-color: #2e2e2e;
        width: 220px;
        height: 360px;
    }
    .film-card img {
        width: 100%;
        height: auto;
        object-fit: cover;
        transition: filter 0.3s ease;
    }
    .film-card:hover img {
        filter: brightness(50%); /* S'assombrir sur hover */
    }
    .film-info {
        position: absolute;
        top: 50%; /* Centrer verticalement */
        left: 0;
        right: 0;
        transform: translateY(-50%); /* Ajustement pour centrer parfaitement */
        padding: 5px;
        font-weight: bold;
        font-size: 12px; /* Taille du texte réduite */
        color: #ffffff;
        background-color: rgba(0, 0, 0, 0.5); /* Fond sombre pour le texte */
        text-align: center; /* Centrer le texte */
        opacity: 0; /* Initialement caché */
        transition: opacity 0.3s ease;
    }
    .film-card:hover .film-info {
        opacity: 1; /* Afficher sur hover */
    }
    .details-container {
        display: flex;
        align-items: flex-start; /* Alignement du texte en haut */
        margin: 20px;
        background-color: #2e2e2e; /* Fond sombre */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(255, 255, 255, 0.2); /* Ombre */
    }
    .details-image {
        width: 250px; /* Augmenter la taille de l'image à 250px */
        height: auto;
        margin-right: 20px; /* Espace entre l'image et le texte */
    }
    .details-title {
        font-size: 24px; /* Taille du titre */
        font-weight: bold;
        color: #FFDD57; /* Couleur du titre */
        border-bottom: 2px solid #FFDD57; /* Ligne sous le titre */
        padding-bottom: 5px; /* Espacement sous le titre */
        margin-bottom: 10px; /* Marge sous le titre */
    }
    .details-section {
        background-color: #3e3e3e; /* Fond légèrement plus clair */
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px; /* Marge entre les sections */
    }
    .details-description, .details-info {
        font-size: 16px; /* Taille de la description */
        color: #cccccc; /* Couleur du texte normal */
        margin: 5px 0; /* Marges entre les lignes */
    }
    .streaming-links {
        margin-top: 10px;
        font-weight: bold;
        color: #FFDD57; /* Couleur des titres de section */
    }
    .streaming-links img {
        width: 30px; /* Réduire la taille des logos de streaming */
        height: auto;
        border-radius: 5px; /* Coins arrondis */
        margin-right: 5px; /* Espacement entre les logos */
    }
        </style>
    """, unsafe_allow_html=True)

# Configurer la page
st.set_page_config(
    page_title="Recherche de films",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Injecter le CSS
inject_css()

# Interface principale
def page():
    query_params = st.query_params

    if "film_id" in query_params:
        film_id = query_params["film_id"]
        afficher_details_film(film_id)
    else:
        st.title("Recherche de films")
        nom_film = st.text_input("Entrez le nom du film :")

        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button("Rechercher"):
                rechercher_films(nom_film)

if __name__ == "__main__":
    page()

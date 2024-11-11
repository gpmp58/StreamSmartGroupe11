import streamlit as st
import requests

from src.webservice.business_object.film import Film

# Configuration de la page

# Injecter le CSS global
def inject_css():
    st.markdown("""
    <style>
    .reportview-container {
        background-color: #1e1e1e; /* Couleur de fond sombre */
    }
    .sidebar .sidebar-content {
        background-color: #2e2e2e; /* Couleur de fond de la barre latérale */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff; /* Couleur des titres */
    }
    p, li {
        color: #cccccc; /* Couleur du texte normal */
    }
    .film-card {
        position: relative;
        overflow: hidden;
        margin: 15px; /* Augmenter la marge pour espacer les cartes */
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(255, 255, 255, 0.3);
        background-color: #2e2e2e;
        width: 160px; /* Réduire la largeur de la carte */
        height: 270px; /* Réduire la hauteur de la carte */
        margin-right: 20px;
        margin-left: 20px
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
        background-color: #FFDD57; /* Couleur jaune pour le fond */
        padding: 10px;  /* Espacement autour de l'image pour laisser de la place au fond */
        border-radius: 10px;  /* Coins arrondis pour le fond */
        display: flex;
        justify-content: center;
        align-items: center;
        width: 350px;  /* Taille plus grande pour l'image */
        height: 450px; /* Hauteur plus grande pour l'image */
        margin-right: 20px; /* Espacement entre l'image et le texte */
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
    .watchlist-button {
        background-color: #FFDD57; /* Jaune lumineux */
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
        background-color: #ffcc00; /* Couleur au survol */
        transform: scale(1.05); /* Légère animation d'agrandissement */
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


# Fonction pour tronquer le texte
def tronquer_texte(texte, max_longueur):
    if len(texte) > max_longueur:
        return texte[:max_longueur] + "..."
    return texte

def rechercher_films(nom_film):
    try:
        # Appel de l'API FastAPI pour rechercher les films
        url = "http://127.0.0.1:8000/films/recherche"  # Lien vers ton endpoint FastAPI
        response = requests.post(url, json={"nom_film": nom_film})
        response.raise_for_status()  # Vérifie les erreurs HTTP

        # Récupération des données des films depuis la réponse JSON
        films = response.json().get("films", {})

        if films:
            film_items = list(films.items())

            for i in range(0, len(film_items), 4):
                cols = st.columns(4)

                for j, (film_id, film_name) in enumerate(film_items[i:i+4]):
                    film = Film(film_id)
                    with cols[j]:
                        description = film.details.get("description", "Pas de description disponible.")
                        description_tronquee = tronquer_texte(description, 300)  # Tronquer à 300 caractères

                        # Vérifie si l'image est disponible, sinon met une image noire
                        image_url = film.image if film.image and film.image != "Image non disponible" else "https://via.placeholder.com/250x360/000000/000000?text=Image+non+disponible"

                        st.markdown(f"""
                            <a href="/?film_id={film_id}" target="_self" style="text-decoration: none;">
                                <div class="film-card">
                                    <img src="{image_url}" alt="{film_name}" />
                                    <div class="film-info">
                                        {description_tronquee} <!-- Afficher le résumé ici -->
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
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'appel API: {e}")



def afficher_details_film(film_id):
    film = Film(film_id)  # Récupérer les détails du film
    st.title(film.details.get("name", "Titre non disponible"))

    # Conteneur pour l'image et les informations
    details_container = st.container()
    with details_container:
        col1, col2 = st.columns([1, 2])
        with col1:
            # Ajouter un carré jaune autour de l'image
            if film.image != "Image non disponible":
                st.markdown(f"""
                    <div class="details-image">
                        <img src="{film.image}" alt="{film.details.get('name', 'Titre non disponible')}" width="300" height="400"/>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Affichage d'une image noire de remplacement si l'image est manquante
                st.markdown(f"""
                    <div class="details-image">
                        <img src="https://via.placeholder.com/250x360/000000/000000?text=Image+non+disponible" alt="Image non disponible" width="300" height="400"/>
                    </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div class='details-title'>{film.details.get('name', 'Titre non disponible')} </div>", unsafe_allow_html=True)

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

            streaming_sites = film.streaming  # Assurez-vous que cette méthode renvoie bien une liste de sites

            if not streaming_sites:
                st.write("Pas de plateformes de streaming disponibles.")
            else:
                st.markdown("<div class='streaming-links'>Disponibles sur :</div>", unsafe_allow_html=True)

                # Créer une grille de 3 colonnes pour les logos de streaming
                cols = st.columns(len(streaming_sites))

                for i, site in enumerate(streaming_sites):
                    logo_url = site.get("logo")
                    site_url = site.get("id")

                    if logo_url and site_url:
                        with cols[i]:
                            st.markdown(f"""
                                <div style='border: 1px solid #444; padding: 10px; border-radius: 10px; background-color: #333;
                                            display: flex; justify-content: center; align-items: center; height: 60px; width : 60px'>
                                    <a href='{site_url}' target='_blank'>
                                        <img src='https://image.tmdb.org/t/p/w45{logo_url}' alt='{site["name"]}'
                                            style='width: 50px; height: auto; border-radius: 5px;' />
                                    </a>
                                </div>
                            """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            # Bouton "Ajouter à la watchlist"
            st.markdown("""<button class="watchlist-button">Ajouter à la watchlist</button>""", unsafe_allow_html=True)



# Interface principale avec Streamlit
def page():
    inject_css()
    query_params = st.query_params  # Utiliser la bonne méthode

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
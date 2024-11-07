import streamlit as st
from src.webservice.services.service_film import FilmService
from src.webservice.business_object.film import Film

# Configuration de la page
st.set_page_config(
    page_title="Recherche de films",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Définir le thème sombre
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
                        description_tronquee = tronquer_texte(description, 300)  # Tronquer à 300 caractères

                        st.markdown(f"""
                            <a href="/?film_id={film_id}" target="_self" style="text-decoration: none;">
                                <div class="film-card">
                                    {f'<img src="{film.image}" alt="{film_name}"/>' if film.image else ''}
                                    <div class="film-info">
                                        {description_tronquee} <!-- Afficher le résumé ici -->
                                    </div>
                                    <div class="placeholder-image" style="{'display: none;' if film.image else ''}">
                                        Image non disponible
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

# Fonction pour afficher les détails du film
# ... (le reste du code reste inchangé)

# Fonction pour afficher les détails du film
def afficher_details_film(film_id):
    film = Film(film_id)  # Récupérer les détails du film
    st.title(film.details.get("title", "Titre non disponible"))

    # Conteneur pour l'image et les informations
    details_container = st.container()
    with details_container:
        col1, col2 = st.columns([1, 2])
        with col1:
            if film.image:
                st.image(film.image, use_column_width=False, width=250)  # Ajuste la taille de l'image à 250px
            else:
                st.write("Image non disponible.")

        with col2:
            st.markdown(f"<div class='details-title'>{film.details.get('title', 'Titre non disponible')}</div>", unsafe_allow_html=True)

            # Section pour la description
            st.markdown("<div class='details-section'>", unsafe_allow_html=True)
            st.markdown(f"<div class='details-description'>{film.details.get('description', 'Pas de description disponible.')}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Informations sur le film
            st.markdown("<div class='details-section'>", unsafe_allow_html=True)
            st.markdown(f"<div class='details-info'>Date de sortie : {film.details.get('date_sortie', 'Date non disponible')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='details-info'>Durée : {film.details.get('duree', 'Durée non disponible')} minutes</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='details-info'>Genres : {', '.join(film.details.get('genres', ['Pas de genres disponibles']))}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Recherche des sites de streaming
            streaming_sites = film.streaming  # Assurez-vous que cette méthode existe
            if streaming_sites:
                st.markdown("<div class='streaming-links'>Disponibles sur :</div>", unsafe_allow_html=True)

                # Conteneur flex pour les logos
                st.markdown("<div style='display: flex; flex-wrap: wrap; margin-top: 10px;'>", unsafe_allow_html=True)
                for site in streaming_sites:
                    if "logo" in site:  # Vérifie que l'image du logo existe
                        st.markdown(f"""
                            <div style='margin-right: 10px;'>
                                <a href='{site["id"]}' target='_blank'>
                                    <img src='https://image.tmdb.org/t/p/w45{site["logo"]}' alt='{site["name"]}' style='width: 30px; height: auto; border-radius: 5px;' />
                                </a>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.write(f"Pas de logo pour {site['name']}.")
                st.markdown("</div>", unsafe_allow_html=True)  # Ferme le conteneur flex

                if len(streaming_sites) == 0:
                    st.write("Pas de plateformes de streaming disponibles.")


# Interface principale avec Streamlit
def main():
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
    main()

# Interface principale avec Streamlit
def page():
    query_params = st.get_query_params()

    if "film_id" in query_params:
        film_id = query_params["film_id"][0]
        afficher_details_film(film_id)
    else:
        st.title("Recherche de films")
        nom_film = st.text_input("Entrez le nom du film :")

        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button("Rechercher"):
                rechercher_films(nom_film)

# Appeler la fonction `page()` pour l'exécution principale
if __name__ == "__main__":
    page()

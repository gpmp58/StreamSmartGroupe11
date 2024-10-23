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
    .placeholder-image {
        background-color: #000; /* Couleur de fond noire */
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        color: #ffffff; /* Couleur du texte */
        font-size: 14px;
        font-weight: bold;
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        transform: translateY(-50%); /* Ajustement pour centrer parfaitement */
        text-align: center; /* Centrer le texte */
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
                        description_tronquee = tronquer_texte(description, 60)  # Tronquer à 60 caractères

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
def afficher_details_film(film_id):
    film = Film(film_id)  # Récupérer les détails du film
    st.write(f"ID du film : {film_id}")  # Affiche l'ID du film
    st.title(film.details.get("title", "Titre non disponible"))
    st.image(film.image, use_column_width=True)  # Affiche l'image du film
    st.write(film.details.get("description", "Pas de description disponible."))

# Interface principale avec Streamlit
def main():
    query_params = st.query_params  # Utiliser la bonne méthode
    st.write("Query Params : ", query_params)  # Ajoute ceci pour déboguer

    if "film_id" in query_params:
        film_id = query_params["film_id"]
        st.write(f"Film ID récupéré : {film_id}")  # Affiche l'ID récupéré
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

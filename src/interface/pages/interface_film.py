import streamlit as st
import requests
from src.interface.main_interface import afficher_etat_connexion

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
    .details-container {
        display: flex;
        align-items: flex-start;
        margin: 20px;
        background-color: #2e2e2e;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(255, 255, 255, 0.2);
    }
    .details-title {
        font-size: 24px;
        font-weight: bold;
        color: #FFDD57;
        border-bottom: 2px solid #FFDD57;
        padding-bottom: 5px;
        margin-bottom: 10px;
    }
    .streaming-links img {
        width: 30px;
        height: auto;
        border-radius: 5px;
        margin-right: 5px;
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

# Initialisation de l'état de session si nécessaire
if 'pseudo' not in st.session_state:
    st.session_state['pseudo'] = None
if 'id_utilisateur' not in st.session_state:
    st.session_state['id_utilisateur'] = None

# Barre latérale pour afficher les informations de l'utilisateur
with st.sidebar:
    if st.session_state['pseudo']:
        st.write(f"**Utilisateur :** {st.session_state['pseudo']}")
        st.write(f"**ID Utilisateur :** {st.session_state['id_utilisateur']}")
        st.write("**État : Connecté**")
    else:
        st.write("Utilisateur : Non connecté")
        st.write("État : Déconnecté")

# Fonction pour tronquer le texte
def tronquer_texte(texte, max_longueur):
    if len(texte) > max_longueur:
        return texte[:max_longueur] + "..."
    return texte

# Fonction pour rechercher les films via l'API locale
def rechercher_films(nom_film):
    try:
        # Endpoint pour rechercher des films
        url = "http://127.0.0.1:8000/films/recherche"
        response = requests.post(url, json={"nom_film": nom_film})
        response.raise_for_status()  # Gérer les erreurs HTTP
        films = response.json().get("films", {})

        if films:
            film_items = list(films.items())
            for i in range(0, len(film_items), 4):
                cols = st.columns(4)
                for j, (film_id, film_name) in enumerate(film_items[i:i+4]):
                    # Récupération des détails du film
                    details_url = f"http://127.0.0.1:8000/films/{film_id}"
                    film_response = requests.get(details_url)
                    if film_response.status_code == 200:
                        film_details = film_response.json()
                    else:
                        continue

                    description = film_details.get("description", "Pas de description disponible.")
                    description_tronquee = tronquer_texte(description, 300)

                    # Vérifie si l'image est disponible
                    image_url = film_details.get("image", "https://via.placeholder.com/250x360/000000/000000?text=Image+non+disponible")

                    with cols[j]:
                        st.markdown(f"""
                            <a href="/interface_details_film?film_id={film_id}" target="_self" style="text-decoration: none;">
                                <div class="film-card">
                                    <img src="{image_url}" alt="{film_name}" />
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
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'appel API: {e}")

# Interface principale avec Streamlit
def page():
    inject_css()

    st.title("Recherche de films")
    nom_film = st.text_input("Entrez le nom du film :")

    if st.button("Rechercher"):
        rechercher_films(nom_film)

if __name__ == "__main__":
    page()

import streamlit as st
import requests

# Configuration de la page principale
st.set_page_config(page_title="Ajouter un Film à une Watchlist", layout="wide")

# URL de base de l'API
LIEN_API = "http://127.0.0.1:8000"

# Initialisation de l'état de session
if 'pseudo' not in st.session_state or 'id_utilisateur' not in st.session_state:
    st.session_state['pseudo'] = None
    st.session_state['id_utilisateur'] = None
if 'id_film_selected' not in st.session_state:
    st.session_state['id_film_selected'] = None
"""
# Vérification de la connexion
if not st.session_state['pseudo']:
    st.error("Vous devez être connecté pour accéder à cette page.")
    st.stop()  # Bloque l'exécution si l'utilisateur n'est pas connecté

# Vérification de l'ID du film
film_id = st.session_state.get('id_film_selected')
if not film_id:
    st.warning("Aucun ID de film fourni. Veuillez rediriger depuis la page des détails du film.")
    st.stop()
"""
# Affichage des informations utilisateur
with st.sidebar:
    st.write(f"**Utilisateur :** {st.session_state['pseudo']}")
    st.write(f"**ID Utilisateur :** {st.session_state['id_utilisateur']}")
    if st.button("Se déconnecter"):
        st.session_state['pseudo'] = None
        st.session_state['id_utilisateur'] = None
        st.rerun()

# Interface pour ajouter un film à une watchlist
st.title("🎥 Ajouter un Film à une Watchlist")

# Champ pour le numéro de la watchlist
numero_watchlist = st.number_input("Numéro de la watchlist", min_value=1, step=1)

# Champ pré-rempli pour l'ID du film (non modifiable)
st.text_input("Numéro du film", value=film_id, disabled=True, key="numero_film")

# Bouton pour ajouter le film
if st.button("Ajouter le Film"):
    if not numero_watchlist:
        st.warning("Veuillez remplir le numéro de la watchlist.")
    else:
        data = {"id_watchlist": numero_watchlist, "id_film": film_id}
        try:
            response = requests.post(f"{LIEN_API}/watchlists/ajouter_film", json=data)
            if response.status_code == 200:
                st.success("✅ Film ajouté à la watchlist avec succès !")
            else:
                st.error(f"Erreur : {response.json().get('detail', 'ERREUR INCONUE')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion à l'API : {e}")

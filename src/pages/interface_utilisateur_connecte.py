import streamlit as st
from src.main_interface import afficher_etat_connexion

# Configuration de la page principale
st.set_page_config(page_title="Utilisateur connecté ", layout="wide")

# Initialisation de l'état de session si nécessaire
if 'pseudo' not in st.session_state:
    st.session_state['pseudo'] = None

# Barre latérale pour afficher les informations de l'utilisateur
with st.sidebar:
    if st.session_state['pseudo']:
        st.write(f"**Utilisateur :** {st.session_state['pseudo']}")
        st.write("**État : Connecté**")
    else:
        st.write("Utilisateur : Non connecté")
        st.write("État : Déconnecté")

st.title("Bienvenue dans l'Application Multi-Page")
st.write("Sélectionnez une option ci-dessous pour naviguer vers la page correspondante.")

st.markdown("---")  # Ligne de séparation

# Affichage des fonctionnalités supplémentaires
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Films"):
        st.switch_page("pages/interface_film.py")

with col2:
    if st.button("Watchlist"):
        st.switch_page("pages/interface_watchlist.py")

with col3:
    if st.button("Se déconnecter"):
        st.session_state['pseudo'] = None
        st.write("Déconnexion ...")
        st.rerun()
